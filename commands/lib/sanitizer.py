"""
Hefesto Skill Generator - Input Sanitization Module

Implements security validation (FR-031, T0-HEFESTO-11).
Protects against shell injection, prompt injection, and path traversal attacks.
"""

import re
import shlex
from pathlib import Path
from typing import List

# Input length limits
MAX_DESCRIPTION_LENGTH = 2000  # T0-HEFESTO-01
MAX_SKILL_NAME_LENGTH = 64  # T0-HEFESTO-07
MAX_SKILL_CONTENT_LENGTH = 500 * 100  # ~500 lines * 100 chars/line

# Allowed skill directories (prevents path traversal)
ALLOWED_SKILL_DIRECTORIES = [
    ".claude/skills",
    ".gemini/skills",
    ".codex/skills",
    ".copilot/skills",
    ".opencode/skills",
    ".cursor/skills",
    ".qwen/skills",
]

# Prompt injection patterns (based on ADR-002 research)
PROMPT_INJECTION_PATTERNS = [
    # Direct command injection
    r"ignore\s+(previous|all|above)\s+instructions",
    r"disregard\s+(previous|all)\s+(instructions|prompts)",
    r"forget\s+(everything|all|previous)",
    # Role manipulation
    r"you\s+are\s+now",
    r"act\s+as\s+a",
    r"pretend\s+to\s+be",
    # System prompt extraction
    r"show\s+(me\s+)?(your|the)\s+(system|initial)\s+prompt",
    r"what\s+(are|is)\s+your\s+instructions",
    # Encoded attacks (base64, unicode tricks)
    r"[A-Za-z0-9+/=]{50,}",  # Likely base64
    # SQL injection patterns (defensive)
    r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION)\b.*\b(FROM|INTO|TABLE)\b)",
    # Path traversal
    r"\.\./|\.\.\\",
]


class ValidationError(Exception):
    """Raised when input validation fails"""

    pass


def validate_length(input_str: str, max_length: int, field_name: str) -> None:
    """
    Validate input length to prevent DoS attacks.

    Args:
        input_str: Input to validate
        max_length: Maximum allowed length
        field_name: Name of field for error message

    Raises:
        ValidationError: If input exceeds max_length
    """
    if len(input_str) > max_length:
        raise ValidationError(
            f"{field_name} exceeds maximum length of {max_length} characters"
        )


def detect_injection_attempt(user_input: str) -> bool:
    """
    Check if input matches known injection patterns.

    Args:
        user_input: Input to check

    Returns:
        True if suspicious pattern detected, False otherwise
    """
    user_input_lower = user_input.lower()

    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, user_input_lower, re.IGNORECASE):
            return True

    # Check for null bytes (can break string handling)
    if "\x00" in user_input:
        return True

    return False


def sanitize_skill_name(name: str) -> str:
    """
    Sanitize skill name to T0-HEFESTO-07 format.

    Auto-sanitizes rather than rejecting (user-friendly approach).

    Args:
        name: Raw skill name input

    Returns:
        Sanitized skill name

    Raises:
        ValidationError: If final name is invalid after sanitization
    """
    # Convert to lowercase
    name = name.lower()

    # Replace non-alphanumeric (except hyphens) with hyphens
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[-\s]+", "-", name)

    # Remove leading/trailing hyphens
    name = name.strip("-")

    # Enforce max length
    name = name[:MAX_SKILL_NAME_LENGTH]

    # Validate final format
    if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name):
        raise ValidationError(
            f"Invalid skill name '{name}'. Must be lowercase alphanumeric with hyphens."
        )

    return name


def sanitize_for_shell(user_input: str) -> str:
    """
    Escape user input for safe shell command usage.

    Args:
        user_input: Input to sanitize

    Returns:
        Shell-escaped string
    """
    return shlex.quote(user_input)


def validate_skill_path(skill_name: str, cli_name: str) -> Path:
    """
    Validate that constructed path stays within allowed directories.

    Prevents path traversal attacks.

    Args:
        skill_name: Sanitized skill name
        cli_name: CLI identifier

    Returns:
        Validated skill path

    Raises:
        ValidationError: If path escapes project directory or not in allowed dirs
    """
    # Sanitize inputs first
    skill_name = sanitize_skill_name(skill_name)

    # Construct path
    skill_path = Path(f".{cli_name}/skills/{skill_name}")

    # Resolve to absolute path (follows symlinks, resolves ..)
    try:
        abs_path = skill_path.resolve()
    except Exception as e:
        raise ValidationError(f"Invalid skill path: {skill_path}") from e

    # Check that resolved path is within project directory
    project_root = Path.cwd().resolve()
    if not str(abs_path).startswith(str(project_root)):
        raise ValidationError(f"Security: Path {abs_path} escapes project directory")

    # Check that path starts with allowed directory
    relative = abs_path.relative_to(project_root)
    if not any(
        str(relative).startswith(allowed) for allowed in ALLOWED_SKILL_DIRECTORIES
    ):
        raise ValidationError(
            f"Security: Path {relative} not in allowed skill directories"
        )

    return skill_path


def validate_user_input(user_input: str, field_name: str, max_length: int) -> None:
    """
    Full input validation pipeline.

    Args:
        user_input: Input to validate
        field_name: Name of field for error messages
        max_length: Maximum allowed length

    Raises:
        ValidationError: If validation fails
    """
    # Check length
    validate_length(user_input, max_length, field_name)

    # Check for injection patterns
    if detect_injection_attempt(user_input):
        from .audit import log_security_event

        log_security_event(
            "validation_failed",
            {
                "field": field_name,
                "input_length": len(user_input),
                "pattern_detected": True,
            },
        )
        raise ValidationError(
            f"Security: {field_name} contains suspicious patterns. "
            f"Please provide standard input without special commands."
        )

    # Check for null bytes
    if "\x00" in user_input:
        raise ValidationError(f"{field_name} contains invalid characters")


def wizard_get_input(
    prompt: str,
    field_name: str,
    max_length: int,
    validator=None,
    max_attempts: int = 3,
) -> str:
    """
    Secure input collection with validation for wizard mode.

    Args:
        prompt: Input prompt to display
        field_name: Name of field being collected
        max_length: Maximum input length
        validator: Optional custom validator function
        max_attempts: Maximum validation attempts

    Returns:
        Validated user input or None if max attempts exceeded

    Raises:
        ValidationError: If input fails validation after max_attempts
    """
    attempts = 0

    while attempts < max_attempts:
        user_input = input(prompt).strip()

        try:
            # Basic validation
            validate_user_input(user_input, field_name, max_length)

            # Custom validation (e.g., skill name format)
            if validator:
                user_input = validator(user_input)

            return user_input

        except ValidationError as e:
            attempts += 1
            print(f"Error: {e}")

            # Log potential attack
            if "Security:" in str(e):
                from .audit import log_security_event

                log_security_event(
                    "validation_failed",
                    {
                        "field": field_name,
                        "input_length": len(user_input),
                    },
                )

            if attempts < max_attempts:
                print(
                    f"Please try again ({max_attempts - attempts} attempts remaining)"
                )
            else:
                print("Maximum attempts reached. Aborting.")
                raise ValidationError(
                    f"Failed to get valid input for {field_name} after {max_attempts} attempts"
                )

    return None
