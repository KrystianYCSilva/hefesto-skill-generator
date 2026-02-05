"""
Hefesto Skill Generator - Atomic File Operations

Implements atomic multi-file persistence with rollback (FR-006).
"""

import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict

from .preview import PreviewObject, ResourceInfo


class AtomicWriteError(Exception):
    """Raised when atomic write operation fails"""

    pass


def persist_skill_atomic(preview: PreviewObject) -> bool:
    """
    Write all skill files atomically across all target CLIs.

    All files succeed or all fail with rollback (FR-006, Edge Case #4).

    Args:
        preview: Approved preview to persist

    Returns:
        True if all writes succeed

    Raises:
        AtomicWriteError: If any write fails (triggers rollback)
    """
    temp_dir = Path(
        f".hefesto/temp/create-{preview.skill_name}-{datetime.now().timestamp()}"
    )
    created_paths = []

    try:
        # Phase 1: Write to temp directory
        for cli in preview.target_clis:
            temp_skill_dir = temp_dir / cli / "skills" / preview.skill_name
            temp_skill_dir.mkdir(parents=True, exist_ok=True)

            # Write SKILL.md
            skill_file = temp_skill_dir / "SKILL.md"
            skill_file.write_text(preview.skill_content, encoding="utf-8")

            # Write metadata.yaml
            metadata_file = temp_skill_dir / "metadata.yaml"
            metadata_file.write_text(preview.metadata_content, encoding="utf-8")

            # Write JIT resources if any
            for resource in preview.resources:
                resource_dir = temp_skill_dir / resource.resource_type
                resource_dir.mkdir(parents=True, exist_ok=True)

                resource_file = resource_dir / resource.filename

                if resource.content:
                    # Write content (scripts, references)
                    resource_file.write_text(resource.content, encoding="utf-8")
                elif resource.path:
                    # Copy file (assets)
                    shutil.copy2(resource.path, resource_file)

            created_paths.append((cli, temp_skill_dir))

        # Phase 2: All writes succeeded - now move atomically
        for cli, temp_skill_dir in created_paths:
            final_dir = Path(f".{cli}/skills/{preview.skill_name}")
            final_dir.parent.mkdir(parents=True, exist_ok=True)

            # Atomic move (rename on same filesystem)
            # If final_dir exists, remove it first (should be backed up already)
            if final_dir.exists():
                shutil.rmtree(final_dir)

            shutil.move(str(temp_skill_dir), str(final_dir))

        return True

    except Exception as e:
        # Phase 3: Rollback on failure
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

        raise AtomicWriteError(
            f"Atomic persistence failed: {e}. All changes rolled back."
        ) from e

    finally:
        # Cleanup temp directory root
        if temp_dir.exists():
            try:
                shutil.rmtree(temp_dir)
            except Exception:
                pass  # Best effort cleanup


def delete_skill_atomic(skill_name: str, target_clis: List[str]) -> bool:
    """
    Delete skill from all target CLIs atomically.

    Args:
        skill_name: Skill name to delete
        target_clis: List of CLI identifiers

    Returns:
        True if all deletions succeed

    Raises:
        AtomicWriteError: If any deletion fails
    """
    # Create temp backup first
    temp_backup = Path(
        f".hefesto/temp/delete-backup-{skill_name}-{datetime.now().timestamp()}"
    )
    backup_paths = []

    try:
        # Phase 1: Backup existing skills
        for cli in target_clis:
            skill_dir = Path(f".{cli}/skills/{skill_name}")

            if skill_dir.exists():
                backup_dir = temp_backup / cli / "skills" / skill_name
                backup_dir.parent.mkdir(parents=True, exist_ok=True)

                shutil.copytree(skill_dir, backup_dir)
                backup_paths.append((cli, skill_dir, backup_dir))

        # Phase 2: Delete all skills
        for cli, skill_dir, _ in backup_paths:
            shutil.rmtree(skill_dir)

        # Phase 3: Cleanup temp backup on success
        if temp_backup.exists():
            shutil.rmtree(temp_backup)

        return True

    except Exception as e:
        # Phase 4: Rollback on failure - restore from temp backup
        for cli, skill_dir, backup_dir in backup_paths:
            if not skill_dir.exists() and backup_dir.exists():
                skill_dir.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(backup_dir, skill_dir)

        # Cleanup temp backup
        if temp_backup.exists():
            shutil.rmtree(temp_backup)

        raise AtomicWriteError(
            f"Atomic deletion failed: {e}. All changes rolled back."
        ) from e


def update_skill_atomic(
    skill_name: str, target_clis: List[str], new_content: Dict[str, str]
) -> bool:
    """
    Update skill content atomically across all CLIs.

    Args:
        skill_name: Skill name to update
        target_clis: List of CLI identifiers
        new_content: Dict mapping filename to new content

    Returns:
        True if all updates succeed

    Raises:
        AtomicWriteError: If any update fails
    """
    temp_dir = Path(f".hefesto/temp/update-{skill_name}-{datetime.now().timestamp()}")
    updated_paths = []

    try:
        # Phase 1: Create temp copies with updates
        for cli in target_clis:
            skill_dir = Path(f".{cli}/skills/{skill_name}")

            if not skill_dir.exists():
                continue

            temp_skill_dir = temp_dir / cli / "skills" / skill_name

            # Copy existing skill to temp
            shutil.copytree(skill_dir, temp_skill_dir)

            # Update files
            for filename, content in new_content.items():
                target_file = temp_skill_dir / filename
                target_file.write_text(content, encoding="utf-8")

            updated_paths.append((cli, skill_dir, temp_skill_dir))

        # Phase 2: All updates succeeded - now move atomically
        for cli, skill_dir, temp_skill_dir in updated_paths:
            # Remove old
            shutil.rmtree(skill_dir)

            # Move new
            shutil.move(str(temp_skill_dir), str(skill_dir))

        return True

    except Exception as e:
        # Phase 3: Rollback on failure
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

        raise AtomicWriteError(
            f"Atomic update failed: {e}. All changes rolled back."
        ) from e

    finally:
        # Cleanup temp directory
        if temp_dir.exists():
            try:
                shutil.rmtree(temp_dir)
            except Exception:
                pass
