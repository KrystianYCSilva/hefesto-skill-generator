"""
Hefesto Skill Generator - Collision Module

Collision detection and resolution for existing skills (FR-020 to FR-025).
"""

import yaml
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from .backup import create_backup, BackupError
from .diff import merge_sections
from .timeout import input_with_timeout
from .colors import bold, cyan, yellow, red, warning, success, error as error_msg
from .audit import log_operation


@dataclass
class CollisionInfo:
    """Metadata about existing skill when collision detected"""

    skill_name: str
    cli_name: str
    skill_path: Path
    created_date: Optional[str]
    modified_date: str
    author: Optional[str]
    version: Optional[str]
    file_size: int


@dataclass
class CollisionDecision:
    """Records user's collision resolution choice"""

    decision: str  # 'overwrite' | 'merge' | 'cancel'
    timestamp: str
    affected_clis: List[str]


def get_skill_metadata(skill_path: Path) -> Dict[str, any]:
    """
    Extract metadata from existing skill frontmatter (FR-021).

    Args:
        skill_path: Path to SKILL.md file

    Returns:
        Dictionary with metadata keys
    """
    if not skill_path.exists():
        return {
            "created": None,
            "modified": None,
            "author": None,
            "version": None,
        }

    try:
        # Read file
        content = skill_path.read_text(encoding="utf-8")

        # Get modified date from file stat
        modified_date = datetime.fromtimestamp(skill_path.stat().st_mtime).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # Parse frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter_yaml = parts[1]

                try:
                    data = yaml.safe_load(frontmatter_yaml)

                    return {
                        "created": data.get("created"),
                        "modified": modified_date,
                        "author": data.get("author"),
                        "version": data.get("version"),
                    }
                except yaml.YAMLError:
                    pass

        # Fallback: just file stat
        return {
            "created": None,
            "modified": modified_date,
            "author": None,
            "version": None,
        }

    except Exception:
        return {
            "created": None,
            "modified": None,
            "author": None,
            "version": None,
        }


def detect_collisions(
    skill_name: str, target_clis: List[str]
) -> Dict[str, CollisionInfo]:
    """
    Detect if skill with same name exists in any target CLI directory (FR-020).

    Args:
        skill_name: Sanitized skill name to check
        target_clis: List of CLI identifiers

    Returns:
        Dictionary mapping CLI name to CollisionInfo for each collision detected
    """
    collisions = {}

    for cli in target_clis:
        skill_path = Path(f".{cli}/skills/{skill_name}/SKILL.md")

        if skill_path.exists():
            # Extract metadata (FR-021)
            metadata = get_skill_metadata(skill_path)

            # Get file size
            file_size = skill_path.stat().st_size

            # Create CollisionInfo
            collision = CollisionInfo(
                skill_name=skill_name,
                cli_name=cli,
                skill_path=skill_path,
                created_date=metadata["created"],
                modified_date=metadata["modified"],
                author=metadata["author"],
                version=metadata["version"],
                file_size=file_size,
            )

            collisions[cli] = collision

    return collisions


def prompt_collision_resolution(
    collisions: Dict[str, CollisionInfo],
) -> CollisionDecision:
    """
    Prompt user to resolve collision (FR-022).

    Args:
        collisions: Detected collisions from detect_collisions()

    Returns:
        CollisionDecision with user's choice
    """
    print(f"\n{bold(red('⚠ COLLISION DETECTED'))}")
    print(f"{yellow('=' * 60)}\n")

    # Display collision details
    skill_name = list(collisions.values())[0].skill_name
    print(
        f"Skill '{bold(skill_name)}' already exists in {len(collisions)} location(s):\n"
    )

    for cli, info in collisions.items():
        print(f"{cyan(f'  .{cli}/skills/{skill_name}/SKILL.md')}")
        if info.created_date:
            print(f"    Created: {info.created_date}")
        print(f"    Modified: {info.modified_date}")
        if info.version:
            print(f"    Version: {info.version}")
        if info.author:
            print(f"    Author: {info.author}")
        print(f"    Size: {info.file_size} bytes")
        print()

    # Show resolution options (FR-022)
    print(f"{yellow('-' * 60)}")
    print(f"\n{bold('Resolution options:')}")
    print(f"  {cyan('[overwrite]')} - Replace existing skill (creates backup)")
    print(f"  {cyan('[merge]')}     - Selectively merge changes section-by-section")
    print(f"  {cyan('[cancel]')}    - Abort operation (preserve existing)")

    # Prompt for choice
    while True:
        choice = (
            input_with_timeout(f"\n{bold('Choose action:')} ", timeout_seconds=300)
            .strip()
            .lower()
        )

        if choice in ["overwrite", "o"]:
            return CollisionDecision(
                decision="overwrite",
                timestamp=datetime.now().isoformat(),
                affected_clis=list(collisions.keys()),
            )
        elif choice in ["merge", "m"]:
            return CollisionDecision(
                decision="merge",
                timestamp=datetime.now().isoformat(),
                affected_clis=list(collisions.keys()),
            )
        elif choice in ["cancel", "c"]:
            return CollisionDecision(
                decision="cancel",
                timestamp=datetime.now().isoformat(),
                affected_clis=list(collisions.keys()),
            )
        else:
            print(
                warning(f"Invalid choice '{choice}'. Choose: overwrite, merge, cancel")
            )


def handle_overwrite(
    collisions: Dict[str, CollisionInfo], skill_name: str, new_content: str
) -> Path:
    """
    Create backups and prepare for overwrite (FR-023).

    Args:
        collisions: Skills to be overwritten
        skill_name: Skill name
        new_content: New skill content (for validation)

    Returns:
        Path to backup file

    Raises:
        BackupError: If backup creation fails
    """
    target_clis = list(collisions.keys())

    try:
        # Create backup (FR-023)
        backup_path = create_backup(skill_name, target_clis)

        print(f"\n{success('✓ Backup created:')}")
        print(f"  {cyan(str(backup_path))}")

        # Log operation
        log_operation(
            operation_type="overwrite",
            skill_name=skill_name,
            decision="backup_created",
            metadata={
                "backup_path": str(backup_path),
                "target_clis": target_clis,
            },
        )

        return backup_path

    except BackupError as e:
        # Backup failed - abort overwrite (Edge Case #5)
        print(f"\n{error_msg('✗ Backup creation failed!')}")
        print(f"  {e}")
        print(f"\n{warning('Overwrite aborted. Original skill preserved.')}")

        # Log failure
        log_operation(
            operation_type="overwrite",
            skill_name=skill_name,
            decision="backup_failed",
            metadata={
                "error": str(e),
                "target_clis": target_clis,
            },
        )

        raise


def handle_merge(
    collisions: Dict[str, CollisionInfo], skill_name: str, new_content: str
) -> str:
    """
    Guide user through section-by-section merge (FR-024).

    Args:
        collisions: Existing skills
        skill_name: Skill name
        new_content: New skill content to merge

    Returns:
        Merged skill content
    """
    # For simplicity, merge with first collision (usually same across CLIs)
    first_cli = list(collisions.keys())[0]
    existing_path = collisions[first_cli].skill_path

    # Load existing content
    existing_content = existing_path.read_text(encoding="utf-8")

    # Perform section-by-section merge
    merged_content = merge_sections(existing_content, new_content)

    print(f"\n{success('✓ Merge complete!')}")

    # Log operation
    log_operation(
        operation_type="merge",
        skill_name=skill_name,
        decision="merge_complete",
        metadata={
            "target_clis": list(collisions.keys()),
        },
    )

    return merged_content


def handle_cancel(collisions: Dict[str, CollisionInfo], skill_name: str) -> None:
    """
    Handle cancel decision - preserve existing skill (FR-025).

    Args:
        collisions: Existing skills (preserved)
        skill_name: Skill name
    """
    print(f"\n{success('Operation cancelled.')}")
    print(f"Existing skill '{skill_name}' preserved in {len(collisions)} location(s).")

    # Log operation
    log_operation(
        operation_type="create",
        skill_name=skill_name,
        decision="collision_cancel",
        metadata={
            "target_clis": list(collisions.keys()),
        },
    )
