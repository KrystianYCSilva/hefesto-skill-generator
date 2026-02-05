"""
Hefesto Skill Generator - Wizard Module

Step-by-step wizard for guided skill creation (FR-008 to FR-014).
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple

from .sanitizer import sanitize_skill_name, validate_user_input, ValidationError
from .timeout import input_with_timeout, TimeoutError
from .colors import (
    bold,
    cyan,
    yellow,
    green,
    gray,
    warning,
    success,
    error as error_msg,
)


@dataclass
class WizardState:
    """
    Maintains wizard progress across steps.

    Attributes match contract specification in contracts/wizard.md
    """

    current_step: int
    collected_inputs: Dict[str, str]
    visited_steps: List[int]
    start_timestamp: str
    timeout_at: str = ""

    def can_go_back(self) -> bool:
        """Check if user can go back to previous step"""
        return len(self.visited_steps) > 0

    def go_back(self) -> Optional[Tuple[int, str]]:
        """
        Go back to previous step.

        Returns:
            Tuple of (step_number, previous_value) or None if can't go back
        """
        if not self.can_go_back():
            return None

        # Pop last visited step
        prev_step = self.visited_steps.pop()

        # Get previous value for that step
        step_keys = ["skill_name", "description", "instructions", "resources"]
        if prev_step <= len(step_keys):
            key = step_keys[prev_step - 1]
            prev_value = self.collected_inputs.get(key, "")
            return (prev_step, prev_value)

        return None

    def add_step(self, step_num: int, value: str) -> None:
        """Record step completion"""
        self.visited_steps.append(step_num)

        # Map step number to key
        step_keys = ["skill_name", "description", "instructions", "resources"]
        if step_num <= len(step_keys):
            key = step_keys[step_num - 1]
            self.collected_inputs[key] = value


class WizardTimeoutError(Exception):
    """Raised when wizard times out"""

    def __init__(self, message: str, state_path: Path):
        super().__init__(message)
        self.state_path = state_path


def _save_wizard_state(state: WizardState) -> Path:
    """
    Persist wizard state to .hefesto/temp/ on timeout.

    Args:
        state: WizardState to save

    Returns:
        Path to saved state file
    """
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    state_file = Path(f".hefesto/temp/wizard-state-{timestamp}.json")
    state_file.parent.mkdir(parents=True, exist_ok=True)

    # Serialize to JSON
    state_data = {
        "current_step": state.current_step,
        "collected_inputs": state.collected_inputs,
        "visited_steps": state.visited_steps,
        "start_timestamp": state.start_timestamp,
        "timeout_at": datetime.now().isoformat(),
    }

    state_file.write_text(json.dumps(state_data, indent=2), encoding="utf-8")

    return state_file


def _load_wizard_state(state_path: Path) -> WizardState:
    """
    Load wizard state from JSON file.

    Args:
        state_path: Path to wizard state file

    Returns:
        Restored WizardState

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If JSON is malformed or missing required fields
    """
    if not state_path.exists():
        raise FileNotFoundError(f"Wizard state file not found: {state_path}")

    try:
        state_data = json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in wizard state file: {e}")

    # Validate required fields
    required_fields = [
        "current_step",
        "collected_inputs",
        "visited_steps",
        "start_timestamp",
    ]
    for field in required_fields:
        if field not in state_data:
            raise ValueError(f"Missing required field in wizard state: {field}")

    return WizardState(
        current_step=state_data["current_step"],
        collected_inputs=state_data["collected_inputs"],
        visited_steps=state_data["visited_steps"],
        start_timestamp=state_data["start_timestamp"],
        timeout_at=state_data.get("timeout_at", ""),
    )


def _display_wizard_header(step_num: int, total_steps: int = 4) -> None:
    """Display wizard step header"""
    print(f"\n{bold(cyan('=' * 60))}")
    print(f"{bold(f'Wizard Mode: Create Skill - Step {step_num}/{total_steps}')}")
    print(f"{cyan('=' * 60)}\n")


def _display_final_review(state: WizardState) -> None:
    """
    Show collected inputs before generating preview (FR-014).

    Args:
        state: WizardState with collected inputs
    """
    print(f"\n{bold(cyan('=' * 60))}")
    print(f"{bold('Wizard Review')}")
    print(f"{cyan('=' * 60)}\n")

    print(
        f"{bold('Skill Name:')} {green(state.collected_inputs.get('skill_name', 'N/A'))}"
    )
    print(f"{bold('Description:')} {state.collected_inputs.get('description', 'N/A')}")

    instructions = state.collected_inputs.get("instructions", "")
    if instructions:
        preview = (
            instructions[:100] + "..." if len(instructions) > 100 else instructions
        )
        print(f"{bold('Instructions:')} {gray(preview)}")

    resources = state.collected_inputs.get("resources", "none")
    print(f"{bold('Resources:')} {resources}")

    print(f"\n{cyan('-' * 60)}")


def wizard_step(step_num: int, state: WizardState) -> Optional[str]:
    """
    Execute single wizard step with validation (FR-010, FR-011, FR-012).

    Args:
        step_num: Step number (1-4)
        state: Current wizard state

    Returns:
        User input (validated) or None if 'back' command

    Raises:
        ValidationError: If input fails validation after 3 attempts
        TimeoutError: If step times out (5 minutes)
    """
    _display_wizard_header(step_num)

    # Step-specific prompts and validation
    if step_num == 1:
        # Step 1: Skill Name (FR-013 auto-sanitizes)
        print("Enter a descriptive name for your skill.")
        print(gray("(e.g., 'Code Review', 'API Documentation', 'Testing Strategy')"))
        print(gray("Tip: Use natural language - it will be auto-formatted\n"))

        attempts = 0
        max_attempts = 3

        while attempts < max_attempts:
            try:
                user_input = input_with_timeout(
                    f"{bold('Skill name:')} ", timeout_seconds=300
                ).strip()

                # Check for back command
                if user_input.lower() == "back":
                    if state.can_go_back():
                        return None
                    else:
                        print(warning("Already at first step. Cannot go back."))
                        continue

                # Check for empty
                if not user_input:
                    print(error_msg("Skill name cannot be empty."))
                    attempts += 1
                    continue

                # Sanitize to T0-HEFESTO-07 format (FR-013)
                sanitized = sanitize_skill_name(user_input)

                if sanitized != user_input:
                    print(gray(f"Auto-formatted to: {sanitized}"))

                return sanitized

            except ValidationError as e:
                attempts += 1
                print(error_msg(f"Error: {e}"))
                if attempts < max_attempts:
                    print(
                        f"Please try again ({max_attempts - attempts} attempts remaining)"
                    )
                else:
                    raise

        raise ValidationError(
            f"Failed to get valid skill name after {max_attempts} attempts"
        )

    elif step_num == 2:
        # Step 2: Description (max 1024 chars, FR-011)
        print("Describe what your skill does in 1-2 sentences.")
        print(gray("(Maximum 1024 characters)"))
        print(gray("Example: 'Standardize code reviews following best practices'\n"))

        attempts = 0
        max_attempts = 3

        while attempts < max_attempts:
            try:
                user_input = input_with_timeout(
                    f"{bold('Description:')} ", timeout_seconds=300
                ).strip()

                # Check for back command
                if user_input.lower() == "back":
                    return None

                # Validate
                validate_user_input(user_input, "description", max_length=1024)

                return user_input

            except ValidationError as e:
                attempts += 1
                print(error_msg(f"Error: {e}"))
                if attempts < max_attempts:
                    print(
                        f"Please try again ({max_attempts - attempts} attempts remaining)"
                    )
                else:
                    raise

        raise ValidationError(
            f"Failed to get valid description after {max_attempts} attempts"
        )

    elif step_num == 3:
        # Step 3: Main Instructions (optional for MVP)
        print("Enter the main instructions for using this skill.")
        print(gray("(Optional - press Enter to skip, or type 'back' to go back)"))
        print(gray("You can use the description as instructions for now.\n"))

        user_input = input_with_timeout(
            f"{bold('Instructions [optional]:')} ", timeout_seconds=300
        ).strip()

        # Check for back command
        if user_input.lower() == "back":
            return None

        # If empty, use description as fallback
        if not user_input:
            return state.collected_inputs.get("description", "")

        return user_input

    elif step_num == 4:
        # Step 4: Optional JIT Resources (simplified for MVP)
        print("Add JIT resources? (scripts, references, assets)")
        print(gray("(Optional - press Enter to skip, or type 'back' to go back)\n"))

        user_input = input_with_timeout(
            f"{bold('Resources [optional]:')} ", timeout_seconds=300
        ).strip()

        # Check for back command
        if user_input.lower() == "back":
            return None

        # For MVP, just record intent
        if not user_input:
            return "none"

        return user_input

    else:
        raise ValueError(f"Invalid step number: {step_num}")


def run_wizard(command: str) -> Optional[Dict[str, str]]:
    """
    Execute wizard flow for /hefesto.create or /hefesto.extract (FR-008, FR-009).

    Args:
        command: 'create' or 'extract'

    Returns:
        Dictionary with collected inputs or None if user cancels/timeout

    Raises:
        WizardTimeoutError: If wizard times out (saves state)
    """
    print(f"\n{success('Wizard Mode activated!')}")
    print(gray("Type 'back' at any step to return to the previous step.\n"))

    # Initialize wizard state
    state = WizardState(
        current_step=1,
        collected_inputs={},
        visited_steps=[],
        start_timestamp=datetime.now().isoformat(),
    )

    total_steps = 4

    try:
        while state.current_step <= total_steps:
            # Execute current step
            result = wizard_step(state.current_step, state)

            if result is None:
                # User typed 'back'
                back_result = state.go_back()
                if back_result:
                    prev_step, prev_value = back_result
                    state.current_step = prev_step
                    print(gray(f"\nReturned to step {prev_step}"))
                else:
                    print(warning("Cannot go back from first step"))
                continue

            # Store result and advance
            state.add_step(state.current_step, result)
            state.current_step += 1

        # All steps completed - show final review (FR-014)
        _display_final_review(state)

        # Confirm
        confirmation = (
            input_with_timeout(
                f"\n{bold('Proceed to generation? [yes/no/back]:')} ",
                timeout_seconds=300,
            )
            .strip()
            .lower()
        )

        if confirmation == "back":
            # Go back to last step
            state.current_step = total_steps
            return run_wizard(command)  # Recursive call
        elif confirmation in ["yes", "y", ""]:
            return state.collected_inputs
        else:
            print(warning("Wizard cancelled."))
            return None

    except TimeoutError:
        # Save state and provide resume instructions
        state_file = _save_wizard_state(state)

        print(f"\n{warning('Wizard timed out after 5 minutes.')}")
        print(f"Progress saved to: {cyan(str(state_file))}")
        print(f"\nTo resume, run: {bold(f'/hefesto.resume {state_file}')}")

        raise WizardTimeoutError(
            f"Wizard timed out. State saved to {state_file}", state_file
        )


def resume_wizard(state_path: Path) -> Optional[Dict[str, str]]:
    """
    Resume wizard from saved state after timeout/interrupt.

    Args:
        state_path: Path to wizard state JSON file

    Returns:
        Dictionary with collected inputs or None if user cancels

    Raises:
        FileNotFoundError: If state file doesn't exist
        ValueError: If state file is corrupted
    """
    # Load state
    state = _load_wizard_state(state_path)

    print(f"\n{success('Resuming wizard from saved state...')}")
    print(f"Last step completed: {state.current_step - 1}")
    print(f"Started at: {gray(state.start_timestamp)}\n")

    # Continue from current step
    total_steps = 4

    try:
        while state.current_step <= total_steps:
            result = wizard_step(state.current_step, state)

            if result is None:
                # User typed 'back'
                back_result = state.go_back()
                if back_result:
                    prev_step, prev_value = back_result
                    state.current_step = prev_step
                else:
                    print(warning("Cannot go back from first step"))
                continue

            state.add_step(state.current_step, result)
            state.current_step += 1

        # Show final review
        _display_final_review(state)

        confirmation = (
            input_with_timeout(
                f"\n{bold('Proceed to generation? [yes/no/back]:')} ",
                timeout_seconds=300,
            )
            .strip()
            .lower()
        )

        if confirmation in ["yes", "y", ""]:
            return state.collected_inputs
        else:
            print(warning("Wizard cancelled."))
            return None

    except TimeoutError:
        # Save state again
        state_file = _save_wizard_state(state)
        print(f"\n{warning('Wizard timed out again.')}")
        print(f"State saved to: {cyan(str(state_file))}")
        raise WizardTimeoutError(
            f"Wizard timed out. State saved to {state_file}", state_file
        )
