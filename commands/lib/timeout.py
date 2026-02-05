"""
Hefesto Skill Generator - Timeout Utilities

Cross-platform timeout wrappers for terminal input with 5-minute default (FR-005).
"""

import sys
import threading
from typing import Callable, Any, TypeVar, Optional

T = TypeVar("T")


class TimeoutError(Exception):
    """Raised when operation times out"""

    pass


def _timeout_handler_unix(signum, frame):
    """Signal handler for Unix timeout"""
    raise TimeoutError("Operation timed out after 5 minutes")


def with_timeout(func: Callable[[], T], timeout_seconds: int = 300) -> Optional[T]:
    """
    Execute function with timeout.

    Cross-platform implementation:
    - Unix: Uses signal.alarm()
    - Windows: Uses threading.Timer()

    Args:
        func: Function to execute
        timeout_seconds: Timeout in seconds (default: 300 = 5 minutes)

    Returns:
        Function result or raises TimeoutError

    Raises:
        TimeoutError: If timeout expires
    """
    if sys.platform == "win32":
        # Windows: Use threading.Timer
        return _with_timeout_threading(func, timeout_seconds)
    else:
        # Unix: Use signal.alarm
        return _with_timeout_signal(func, timeout_seconds)


def _with_timeout_signal(func: Callable[[], T], timeout_seconds: int) -> T:
    """
    Unix implementation using signal.alarm().

    Args:
        func: Function to execute
        timeout_seconds: Timeout in seconds

    Returns:
        Function result

    Raises:
        TimeoutError: If timeout expires
    """
    import signal

    # Set up signal handler
    old_handler = signal.signal(signal.SIGALRM, _timeout_handler_unix)

    try:
        # Start alarm
        signal.alarm(timeout_seconds)

        # Execute function
        result = func()

        # Cancel alarm
        signal.alarm(0)

        return result

    finally:
        # Restore old handler
        signal.signal(signal.SIGALRM, old_handler)
        signal.alarm(0)


def _with_timeout_threading(func: Callable[[], T], timeout_seconds: int) -> Optional[T]:
    """
    Windows implementation using threading.Timer().

    Args:
        func: Function to execute
        timeout_seconds: Timeout in seconds

    Returns:
        Function result or None if timeout

    Raises:
        TimeoutError: If timeout expires
    """
    result = [None]
    exception = [None]

    def target():
        try:
            result[0] = func()
        except Exception as e:
            exception[0] = e

    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()

    # Wait for thread with timeout
    thread.join(timeout=timeout_seconds)

    if thread.is_alive():
        # Thread still running after timeout
        raise TimeoutError(f"Operation timed out after {timeout_seconds} seconds")

    # Check if exception occurred
    if exception[0] is not None:
        raise exception[0]

    return result[0]


def input_with_timeout(prompt: str, timeout_seconds: int = 300) -> str:
    """
    Get user input with timeout.

    Args:
        prompt: Input prompt to display
        timeout_seconds: Timeout in seconds (default: 300 = 5 minutes)

    Returns:
        User input string

    Raises:
        TimeoutError: If user doesn't respond within timeout
    """
    print(prompt, end="", flush=True)

    def get_input():
        return input()

    try:
        return with_timeout(get_input, timeout_seconds)
    except TimeoutError:
        print("\n")  # New line after timeout
        raise


class TimeoutContext:
    """
    Context manager for timeout operations.

    Usage:
        with TimeoutContext(300) as timeout:
            user_input = timeout.input("Enter value: ")
    """

    def __init__(self, timeout_seconds: int = 300):
        """
        Initialize timeout context.

        Args:
            timeout_seconds: Timeout in seconds (default: 300 = 5 minutes)
        """
        self.timeout_seconds = timeout_seconds
        self._timer = None

    def __enter__(self):
        """Enter timeout context"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit timeout context and cleanup"""
        if self._timer is not None:
            self._timer.cancel()
        return False

    def input(self, prompt: str) -> str:
        """
        Get input with timeout.

        Args:
            prompt: Input prompt

        Returns:
            User input

        Raises:
            TimeoutError: If timeout expires
        """
        return input_with_timeout(prompt, self.timeout_seconds)

    def execute(self, func: Callable[[], T]) -> T:
        """
        Execute function with timeout.

        Args:
            func: Function to execute

        Returns:
            Function result

        Raises:
            TimeoutError: If timeout expires
        """
        return with_timeout(func, self.timeout_seconds)
