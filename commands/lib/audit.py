"""
Hefesto Skill Generator - Audit and Logging Module

Provides operation logging for audit trail (FR-033).
Logs user decisions, security events, and system operations.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


class AuditLogger:
    """Centralized audit logging for Human Gate operations"""

    def __init__(self, log_dir: Path = None):
        """
        Initialize audit logger.

        Args:
            log_dir: Directory for log files (default: .hefesto/logs/)
        """
        if log_dir is None:
            log_dir = Path(".hefesto/logs")

        self.log_dir = log_dir
        self.operations_log = log_dir / "operations.jsonl"
        self.security_log = log_dir / "security.log"

        # Ensure log directory exists
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def log_operation(
        self,
        operation_type: str,
        skill_name: str,
        decision: str,
        metadata: Dict[str, Any] = None,
    ) -> None:
        """
        Log an operation to the audit trail.

        Args:
            operation_type: Type of operation ('create', 'overwrite', 'merge', 'reject')
            skill_name: Name of skill being operated on
            decision: User's decision ('approve', 'reject', 'expand', 'edit', 'cancel')
            metadata: Additional operation metadata
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation_type,
            "skill_name": skill_name,
            "decision": decision,
            "metadata": metadata or {},
        }

        # Append to JSONL file (one JSON object per line)
        with self.operations_log.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def log_security_event(self, event_type: str, details: Dict[str, Any]) -> None:
        """
        Log a security-relevant event.

        Args:
            event_type: Type of security event
            details: Event details (sanitized, no sensitive data)
        """
        # Sanitize details to avoid logging sensitive user input
        safe_details = {
            "event": event_type,
            "timestamp": datetime.now().isoformat(),
            "input_length": details.get("input_length", 0),
            "field": details.get("field", "unknown"),
            "pattern_detected": details.get("pattern_detected", False),
        }

        # Append to security log
        with self.security_log.open("a", encoding="utf-8") as f:
            f.write(f"{json.dumps(safe_details)}\n")


# Global audit logger instance
_audit_logger = None


def get_audit_logger() -> AuditLogger:
    """Get the global audit logger instance."""
    global _audit_logger
    if _audit_logger is None:
        _audit_logger = AuditLogger()
    return _audit_logger


def log_operation(
    operation_type: str,
    skill_name: str,
    decision: str,
    metadata: Dict[str, Any] = None,
) -> None:
    """Convenience function to log operation to global logger."""
    get_audit_logger().log_operation(operation_type, skill_name, decision, metadata)


def log_security_event(event_type: str, details: Dict[str, Any]) -> None:
    """Convenience function to log security event to global logger."""
    get_audit_logger().log_security_event(event_type, details)
