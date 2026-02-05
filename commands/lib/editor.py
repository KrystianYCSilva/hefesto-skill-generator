"""
Hefesto Skill Generator - Editor Module

External editor integration for inline skill editing (FR-027 to FR-030).
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path

from .colors import warning, error as error_msg


class EditorError(Exception):
    """Raised when editor operations fail"""

    pass


def get_default_editor() -> str:
    """
    Detect user's preferred editor with platform-specific fallbacks.

    Priority: $EDITOR > $VISUAL > platform defaults

    Returns:
        Editor command string

    Raises:
        EditorError: If no editor found
    """
    # Check $EDITOR environment variable first
    editor = os.environ.get("EDITOR")
    if editor:
        return editor

    # Check $VISUAL as fallback
    editor = os.environ.get("VISUAL")
    if editor:
        return editor

    # Platform-specific defaults
    if sys.platform == "win32":
        # Windows: notepad.exe is always available
        return "notepad.exe"
    else:
        # Unix: vim is more commonly installed than nano
        # Check if vim exists, fallback to nano, then vi
        import shutil

        if shutil.which("vim"):
            return "vim"
        elif shutil.which("nano"):
            return "nano"
        elif shutil.which("vi"):
            return "vi"
        else:
            raise EditorError(
                "No editor found. Please set $EDITOR environment variable."
            )


def edit_content(content: str, file_extension: str = ".md") -> str:
    """
    Open content in user's editor, wait for close, return edited content (FR-027).

    Args:
        content: Content to edit
        file_extension: File extension for temp file (default: .md)

    Returns:
        Edited content

    Raises:
        EditorError: If editor fails or not found
    """
    editor_cmd = get_default_editor()

    # Create temporary file
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=file_extension, delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    try:
        print(f"\nOpening editor: {editor_cmd}")
        print(warning("Save and close the editor when done editing.\n"))

        # Launch editor and wait for close
        result = subprocess.run(
            [editor_cmd, tmp_path],
            check=False,  # Don't raise on non-zero exit (some editors exit with 1)
        )

        # Check if editor was terminated abnormally
        if result.returncode not in [0, 1]:
            raise EditorError(f"Editor exited with code {result.returncode}")

        # Read edited content
        edited_content = Path(tmp_path).read_text(encoding="utf-8")

        # Check if content changed
        if edited_content == content:
            print(warning("No changes detected."))

        return edited_content

    except FileNotFoundError:
        raise EditorError(
            f"Editor '{editor_cmd}' not found. "
            f"Set $EDITOR environment variable or install {editor_cmd}."
        )

    except Exception as e:
        raise EditorError(f"Editor failed: {e}") from e

    finally:
        # Cleanup temp file
        try:
            Path(tmp_path).unlink()
        except Exception:
            pass  # Best effort cleanup


def edit_with_retry(content: str, file_extension: str = ".md") -> tuple[str, bool]:
    """
    Edit content with retry on validation failure.

    Args:
        content: Content to edit
        file_extension: File extension for temp file

    Returns:
        Tuple of (edited_content, user_cancelled)
    """
    try:
        edited = edit_content(content, file_extension)
        return edited, False

    except EditorError as e:
        print(f"\n{error_msg(f'Editor error: {e}')}")
        print("Returning to Human Gate without changes.")
        return content, True
