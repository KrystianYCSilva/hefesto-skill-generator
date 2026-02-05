"""
Hefesto Skill Generator - Resume Command Implementation

Resumes interrupted wizard sessions from saved state (FR-011 timeout recovery).
"""

import sys
from pathlib import Path

from lib.wizard import resume_wizard, InvalidStateError
from lib.human_gate import run_human_gate_workflow, TimeoutError, ValidationError
from lib.audit import log_operation
from lib.colors import success, error as error_msg, warning, cyan, bold


def hefesto_resume(args):
    """
    Resume interrupted wizard session from saved state.

    Args:
        args: Argparse namespace with:
            - state_path: str - Path to wizard state JSON file

    Returns:
        int: Exit code (0 = success, 1 = error)
    """
    state_path = Path(args.state_path)

    # Validate state file exists
    if not state_path.exists():
        print(error_msg(f"State file not found: {state_path}"))
        print("\nAvailable wizard states:")
        temp_dir = Path(".hefesto/temp")
        if temp_dir.exists():
            state_files = list(temp_dir.glob("wizard-state-*.json"))
            if state_files:
                for f in sorted(
                    state_files, key=lambda p: p.stat().st_mtime, reverse=True
                ):
                    mtime = f.stat().st_mtime
                    from datetime import datetime

                    mtime_str = datetime.fromtimestamp(mtime).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    print(f"  {cyan(f.name)} (saved: {mtime_str})")
            else:
                print("  (none)")
        else:
            print("  (none)")
        return 1

    print(bold("Resuming wizard session..."))
    print(f"State file: {cyan(str(state_path))}\n")

    try:
        # Resume wizard from saved state
        preview = resume_wizard(state_path)

        if preview is None:
            # User cancelled during wizard
            print("\n")
            print(success("Wizard cancelled by user."))
            log_operation(
                operation_type="resume",
                skill_name="unknown",
                decision="cancel",
                metadata={"state_path": str(state_path)},
            )
            return 0

        # Wizard completed - proceed to Human Gate
        print("\n")
        print(cyan("=" * 60))
        print(bold("Wizard Complete - Proceeding to Human Gate"))
        print(cyan("=" * 60))

        result = run_human_gate_workflow(preview)

        if result:
            # Cleanup state file after successful completion
            try:
                state_path.unlink()
            except Exception:
                pass  # Best effort cleanup

            log_operation(
                operation_type="resume",
                skill_name=preview.skill_name,
                decision="approve",
                metadata={"state_path": str(state_path)},
            )
            return 0
        else:
            log_operation(
                operation_type="resume",
                skill_name=preview.skill_name,
                decision="reject",
                metadata={"state_path": str(state_path)},
            )
            return 1

    except FileNotFoundError:
        print(error_msg(f"State file not found: {state_path}"))
        return 1

    except InvalidStateError as e:
        print(error_msg(f"Invalid wizard state: {e}"))
        print("State file may be corrupted. Starting fresh wizard recommended.")
        log_operation(
            operation_type="resume",
            skill_name="unknown",
            decision="error",
            metadata={"state_path": str(state_path), "error": str(e)},
        )
        return 1

    except TimeoutError:
        print(warning("Wizard timed out again. State saved for retry."))
        return 1

    except ValidationError as e:
        print(error_msg(f"Validation error: {e}"))
        return 1

    except KeyboardInterrupt:
        print("\n")
        print(warning("Interrupted by user."))
        return 1

    except Exception as e:
        print(error_msg(f"Unexpected error: {e}"))
        return 1


def main():
    """Entry point for /hefesto.resume command"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Resume interrupted wizard session",
        prog="/hefesto.resume",
    )
    parser.add_argument(
        "state_path",
        type=str,
        help="Path to wizard state JSON file (e.g., .hefesto/temp/wizard-state-2026-02-05T14-30-00.json)",
    )

    args = parser.parse_args()
    sys.exit(hefesto_resume(args))


if __name__ == "__main__":
    main()
