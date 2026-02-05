"""
Hefesto Skill Generator - Human Gate Module

Core Human Gate approval workflow (FR-001 to FR-007).
Implements T0-HEFESTO-02: No file writes without explicit human approval.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .preview import PreviewObject, format_preview
from .atomic import persist_skill_atomic, AtomicWriteError
from .timeout import input_with_timeout, TimeoutError
from .audit import log_operation
from .colors import success, error as error_msg, warning, cyan, bold
from .editor import EditorError


@dataclass
class HumanGateDecision:
    """Records user choice at approval gate"""

    decision: str  # 'approve' | 'expand' | 'edit' | 'reject'
    timestamp: str
    response_time: float  # seconds from preview to decision
    preview_id: str


class ValidationError(Exception):
    """Raised when preview validation fails"""

    pass


def _validate_preview(preview: PreviewObject) -> None:
    """
    Ensure preview is ready for Human Gate.

    Args:
        preview: PreviewObject to validate

    Raises:
        ValidationError: If preview is invalid
    """
    if preview.validation_status != "valid":
        raise ValidationError(
            f"Preview validation failed: {', '.join(preview.validation_errors)}"
        )

    if not preview.target_clis:
        raise ValidationError("Preview has no target CLIs")


def present_human_gate(preview: PreviewObject) -> HumanGateDecision:
    """
    Display preview and await user decision with timeout (FR-001 to FR-005).

    Args:
        preview: Validated skill preview to display

    Returns:
        HumanGateDecision with user's choice

    Raises:
        TimeoutError: If 5 minutes elapse without response (FR-005)
        ValidationError: If preview.validation_status != 'valid'
    """
    # Validate preview
    _validate_preview(preview)

    # Display formatted preview (FR-003)
    formatted = format_preview(preview)
    print(formatted)

    # Record start time
    start_time = datetime.now()

    try:
        # Await user input with 5-minute timeout (FR-004, FR-005)
        user_input = input_with_timeout("\n> ", timeout_seconds=300).strip().lower()

        # Calculate response time
        response_time = (datetime.now() - start_time).total_seconds()

        # Validate input
        valid_choices = ["approve", "expand", "edit", "reject"]
        if user_input not in valid_choices:
            print(
                warning(
                    f"Invalid choice '{user_input}'. Please choose: {', '.join(valid_choices)}"
                )
            )
            return present_human_gate(preview)  # Retry

        # Create decision
        decision = HumanGateDecision(
            decision=user_input,
            timestamp=datetime.now().isoformat(),
            response_time=response_time,
            preview_id=preview.timestamp,
        )

        return decision

    except TimeoutError:
        print("\n")
        print(warning("Human Gate timed out after 5 minutes."))
        print("Operation automatically cancelled.")
        raise


def handle_decision(preview: PreviewObject, decision: HumanGateDecision) -> bool:
    """
    Route decision to appropriate handler.

    Args:
        preview: PreviewObject that was approved/rejected
        decision: User's decision

    Returns:
        True if operation should proceed, False if cancelled
    """
    if decision.decision == "approve":
        return _handle_approve(preview, decision)
    elif decision.decision == "reject":
        return _handle_reject(preview, decision)
    elif decision.decision == "expand":
        return _handle_expand(preview)
    elif decision.decision == "edit":
        return _handle_edit(preview)
    else:
        print(error_msg(f"Unknown decision: {decision.decision}"))
        return False


def _handle_approve(preview: PreviewObject, decision: HumanGateDecision) -> bool:
    """
    Handle [approve] decision - persist files atomically (FR-006, FR-007).

    Args:
        preview: Approved preview
        decision: Approval decision

    Returns:
        True if persistence succeeded
    """
    try:
        # Persist files atomically (FR-006)
        persist_skill_atomic(preview)

        # Log operation (FR-033)
        log_operation(
            operation_type="create",
            skill_name=preview.skill_name,
            decision="approve",
            metadata={
                "target_clis": preview.target_clis,
                "response_time": decision.response_time,
                "total_files": preview.total_files(),
            },
        )

        # Display confirmation (FR-007)
        print("\n")
        print(success(f"Skill '{preview.skill_name}' created successfully!"))
        print(f"\n{bold('Created files:')}")
        for cli in preview.target_clis:
            for path in preview.file_paths[cli]:
                print(f"  {cyan('✓')} {path}")

        print(f"\n{bold('Total:')}")
        print(f"  CLIs: {len(preview.target_clis)}")
        print(f"  Files: {preview.total_files()}")
        print(f"  Size: {preview.total_size()} bytes")

        return True

    except AtomicWriteError as e:
        # Atomic rollback already happened
        print("\n")
        print(error_msg(f"Failed to create skill: {e}"))
        print("All changes have been rolled back.")

        # Log failure
        log_operation(
            operation_type="create",
            skill_name=preview.skill_name,
            decision="approve_failed",
            metadata={
                "error": str(e),
                "target_clis": preview.target_clis,
            },
        )

        return False


def _handle_expand(preview: PreviewObject) -> bool:
    """
    Handle [expand] decision - add JIT resources iteratively (FR-015 to FR-019).

    Args:
        preview: PreviewObject to expand with resources

    Returns:
        True if user approves after expansion, False if cancelled
    """
    try:
        from .expansion import prompt_for_resources, update_preview_with_resources

        # Prompt for resources (FR-016, FR-017)
        resources = prompt_for_resources(preview)

        if resources:
            # Update preview with resources (FR-018)
            updated_preview = update_preview_with_resources(preview, resources)

            # Re-display preview with resources
            print("\n")
            print(cyan("=" * 60))
            print(bold("Updated Preview with Resources"))
            print(cyan("=" * 60))

            formatted = format_preview(updated_preview)
            print(formatted)

            # Present Human Gate again with updated preview
            decision = present_human_gate(updated_preview)
            return handle_decision(updated_preview, decision)
        else:
            # No resources added, return to Human Gate
            print("\n")
            print(warning("No resources added. Returning to Human Gate."))
            decision = present_human_gate(preview)
            return handle_decision(preview, decision)

    except Exception as e:
        print("\n")
        print(error_msg(f"Expansion error: {e}"))
        return False


def _handle_edit(preview: PreviewObject) -> bool:
    """
    Handle [edit] decision - open editor, re-validate, update preview (FR-027 to FR-030).

    Args:
        preview: PreviewObject to edit

    Returns:
        True if user approves after editing, False if cancelled
    """
    from .editor import edit_content

    try:
        print("\n")
        print(cyan("=" * 60))
        print(bold("Inline Editing Mode"))
        print(cyan("=" * 60))
        print(f"Opening SKILL.md for '{preview.skill_name}' in editor...")

        edited_content = edit_content(preview.skill_content, file_extension=".md")

        if edited_content == preview.skill_content:
            print("\n")
            print(warning("No changes detected. Returning to Human Gate."))
            decision = present_human_gate(preview)
            return handle_decision(preview, decision)

        # Re-validate edited content (FR-029)
        try:
            from commands.hefesto_create_impl import validate_skill

            validation_errors = validate_skill(edited_content)

            if validation_errors:
                print("\n")
                print(error_msg("Validation failed after editing:"))
                for err in validation_errors[:5]:
                    print(f"  • {err}")
                if len(validation_errors) > 5:
                    print(f"  ... and {len(validation_errors) - 5} more errors")

                # Prompt for retry/discard/abort (FR-029)
                print("\n")
                print(bold("Options:"))
                print("  [retry-edit] - Fix validation errors in editor")
                print("  [discard-changes] - Discard edits and return to original")
                print("  [abort] - Cancel entire operation")

                choice = input_with_timeout("\n> ", timeout_seconds=300).strip().lower()

                if choice == "retry-edit":
                    updated_preview = PreviewObject(
                        skill_name=preview.skill_name,
                        skill_content=edited_content,
                        metadata_content=preview.metadata_content,
                        target_clis=preview.target_clis,
                        validation_status="invalid",
                        validation_errors=validation_errors,
                        file_paths=preview.file_paths,
                        file_sizes=preview.file_sizes,
                        timestamp=datetime.now().isoformat(),
                        resources=preview.resources,
                    )
                    return _handle_edit(updated_preview)

                elif choice == "discard-changes":
                    print("\n")
                    print(success("Changes discarded. Returning to original preview."))
                    decision = present_human_gate(preview)
                    return handle_decision(preview, decision)

                elif choice == "abort":
                    print("\n")
                    print(success("Operation cancelled."))
                    log_operation(
                        operation_type="create",
                        skill_name=preview.skill_name,
                        decision="edit_abort",
                        metadata={"reason": "validation_failed"},
                    )
                    return False

                else:
                    print(warning(f"Invalid choice '{choice}'. Aborting."))
                    return False

            # Validation passed - update preview
            updated_preview = PreviewObject(
                skill_name=preview.skill_name,
                skill_content=edited_content,
                metadata_content=preview.metadata_content,
                target_clis=preview.target_clis,
                validation_status="valid",
                validation_errors=[],
                file_paths=preview.file_paths,
                file_sizes=preview.file_sizes,
                timestamp=datetime.now().isoformat(),
                resources=preview.resources,
            )

            print("\n")
            print(success("Validation passed! Displaying updated preview..."))
            print("\n")
            print(cyan("=" * 60))
            print(bold("Updated Preview"))
            print(cyan("=" * 60))

            decision = present_human_gate(updated_preview)
            return handle_decision(updated_preview, decision)

        except ImportError as e:
            print("\n")
            print(error_msg(f"Validator not found: {e}"))
            print("Cannot re-validate edited content. Aborting.")
            return False

    except EditorError as e:
        print("\n")
        print(error_msg(f"Editor error: {e}"))
        print("Returning to Human Gate without changes.")
        decision = present_human_gate(preview)
        return handle_decision(preview, decision)

    except TimeoutError:
        print("\n")
        print(warning("Edit operation timed out. Returning to Human Gate."))
        decision = present_human_gate(preview)
        return handle_decision(preview, decision)

    except Exception as e:
        print("\n")
        print(error_msg(f"Unexpected error during editing: {e}"))
        return False


def _handle_reject(preview: PreviewObject, decision: HumanGateDecision) -> bool:
    """
    Handle [reject] decision - abort operation with confirmation (FR-004).

    Args:
        preview: Rejected preview
        decision: Rejection decision

    Returns:
        False (operation cancelled)
    """
    # Log operation
    log_operation(
        operation_type="create",
        skill_name=preview.skill_name,
        decision="reject",
        metadata={
            "response_time": decision.response_time,
        },
    )

    # Display confirmation
    print("\n")
    print(success("Operation cancelled. No files were created."))

    return False


# High-level workflow function
def run_human_gate_workflow(preview: PreviewObject) -> bool:
    """
    Complete Human Gate workflow: present preview → get decision → handle.

    This is the main entry point for Human Gate approval.

    Args:
        preview: PreviewObject to present for approval

    Returns:
        True if user approved and files were created, False otherwise

    Raises:
        TimeoutError: If user doesn't respond within 5 minutes
        ValidationError: If preview is invalid
    """
    try:
        # Present Human Gate and get decision
        decision = present_human_gate(preview)

        # Handle decision
        return handle_decision(preview, decision)

    except TimeoutError:
        # Timeout already logged warning message
        # Log to audit trail
        log_operation(
            operation_type="create",
            skill_name=preview.skill_name,
            decision="timeout",
            metadata={
                "timeout_seconds": 300,
            },
        )
        return False

    except ValidationError as e:
        print("\n")
        print(error_msg(f"Validation error: {e}"))
        return False
