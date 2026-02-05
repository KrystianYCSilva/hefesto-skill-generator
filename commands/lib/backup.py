"""
Hefesto Skill Generator - Backup Module

.tar.gz backup creation for skill overwrite protection (FR-023).
"""

import tarfile
from datetime import datetime
from pathlib import Path
from typing import List, Dict


class BackupError(Exception):
    """Raised when backup creation fails"""

    pass


def create_backup(skill_name: str, target_clis: List[str]) -> Path:
    """
    Create .tar.gz backup of existing skill directories (FR-023).

    Args:
        skill_name: Name of skill to backup
        target_clis: List of CLI identifiers

    Returns:
        Path to created backup file

    Raises:
        BackupError: If backup creation fails
    """
    # Generate timestamp (ISO8601 format for filename safety)
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")

    # Backup paths
    backup_dir = Path(".hefesto/backups")
    backup_dir.mkdir(parents=True, exist_ok=True)

    temp_backup = backup_dir / f"{skill_name}-{timestamp}.tar.gz.tmp"
    final_backup = backup_dir / f"{skill_name}-{timestamp}.tar.gz"

    try:
        # Create tar.gz with temp file for atomicity
        with tarfile.open(temp_backup, "w:gz") as tar:
            for cli in target_clis:
                skill_dir = Path(f".{cli}/skills/{skill_name}")

                if skill_dir.exists():
                    # Add entire skill directory to archive
                    # arcname ensures paths are relative in archive
                    tar.add(skill_dir, arcname=f"{cli}/skills/{skill_name}")

        # Atomic rename (succeeds completely or not at all)
        temp_backup.rename(final_backup)

        return final_backup

    except Exception as e:
        # Cleanup temp file on failure
        if temp_backup.exists():
            temp_backup.unlink()

        raise BackupError(f"Failed to create backup: {e}") from e


def restore_backup(backup_path: Path) -> bool:
    """
    Restore skills from backup archive.

    Args:
        backup_path: Path to .tar.gz backup file

    Returns:
        True if restore succeeded

    Raises:
        BackupError: If restore fails
    """
    if not backup_path.exists():
        raise BackupError(f"Backup file not found: {backup_path}")

    try:
        # Extract to project root (archive has relative paths)
        with tarfile.open(backup_path, "r:gz") as tar:
            tar.extractall(path=Path.cwd())

        return True

    except Exception as e:
        raise BackupError(f"Failed to restore backup: {e}") from e
