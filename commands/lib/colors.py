"""
Hefesto Skill Generator - ANSI Color Utilities

Cross-platform ANSI color support with automatic fallback to plain text.
"""

import os
import sys


def _detect_ansi_support() -> bool:
    """
    Detect if terminal supports ANSI color codes.

    Returns:
        True if ANSI supported, False otherwise
    """
    # Check if stdout is a TTY
    if not hasattr(sys.stdout, "isatty") or not sys.stdout.isatty():
        return False

    # Check TERM environment variable
    if os.getenv("TERM") == "dumb":
        return False

    # Windows 10+ supports ANSI natively after initialization
    if sys.platform == "win32":
        try:
            # Enable ANSI support on Windows
            os.system("")  # Initialize ANSI
            return True
        except Exception:
            return False

    # Unix-like systems generally support ANSI
    return True


class Colors:
    """ANSI color codes with automatic fallback"""

    # Detect ANSI support once at module load
    SUPPORTS_COLOR = _detect_ansi_support()

    if SUPPORTS_COLOR:
        # ANSI escape codes
        RESET = "\033[0m"
        BOLD = "\033[1m"
        DIM = "\033[2m"

        # Foreground colors
        BLACK = "\033[30m"
        RED = "\033[31m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        BLUE = "\033[34m"
        MAGENTA = "\033[35m"
        CYAN = "\033[36m"
        WHITE = "\033[37m"
        GRAY = "\033[90m"

        # Background colors
        BG_BLACK = "\033[40m"
        BG_RED = "\033[41m"
        BG_GREEN = "\033[42m"
        BG_YELLOW = "\033[43m"
        BG_BLUE = "\033[44m"
        BG_MAGENTA = "\033[45m"
        BG_CYAN = "\033[46m"
        BG_WHITE = "\033[47m"
    else:
        # Fallback: no colors
        RESET = ""
        BOLD = ""
        DIM = ""

        BLACK = ""
        RED = ""
        GREEN = ""
        YELLOW = ""
        BLUE = ""
        MAGENTA = ""
        CYAN = ""
        WHITE = ""
        GRAY = ""

        BG_BLACK = ""
        BG_RED = ""
        BG_GREEN = ""
        BG_YELLOW = ""
        BG_BLUE = ""
        BG_MAGENTA = ""
        BG_CYAN = ""
        BG_WHITE = ""


def colorize(text: str, color_code: str) -> str:
    """
    Apply color code to text if ANSI supported.

    Args:
        text: Text to colorize
        color_code: ANSI color code (e.g., Colors.GREEN)

    Returns:
        Colored text or plain text if ANSI not supported
    """
    if Colors.SUPPORTS_COLOR and color_code:
        return f"{color_code}{text}{Colors.RESET}"
    return text


def bold(text: str) -> str:
    """Apply bold formatting"""
    return colorize(text, Colors.BOLD)


def red(text: str) -> str:
    """Apply red color"""
    return colorize(text, Colors.RED)


def green(text: str) -> str:
    """Apply green color"""
    return colorize(text, Colors.GREEN)


def yellow(text: str) -> str:
    """Apply yellow color"""
    return colorize(text, Colors.YELLOW)


def blue(text: str) -> str:
    """Apply blue color"""
    return colorize(text, Colors.BLUE)


def cyan(text: str) -> str:
    """Apply cyan color"""
    return colorize(text, Colors.CYAN)


def gray(text: str) -> str:
    """Apply gray color"""
    return colorize(text, Colors.GRAY)


def success(text: str) -> str:
    """Format success message (green checkmark)"""
    return green(f"✓ {text}")


def error(text: str) -> str:
    """Format error message (red cross)"""
    return red(f"✗ {text}")


def warning(text: str) -> str:
    """Format warning message (yellow exclamation)"""
    return yellow(f"⚠ {text}")


def info(text: str) -> str:
    """Format info message (blue info icon)"""
    return blue(f"ℹ {text}")
