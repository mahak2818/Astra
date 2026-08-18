"""
Security Gate module implementing Level 0, Level 1, and Level 2 security checks.
"""

from typing import Callable, Optional
from astra.models.schemas import SecurityLevel, Task, UserConfirmationRequest
from astra.utils.logging import setup_logger

logger = setup_logger("astra.security")


class SecurityGate:
    """Evaluates security clearance for capability actions."""

    def __init__(self, confirmation_callback: Optional[Callable[[UserConfirmationRequest], bool]] = None):
        self.confirmation_callback = confirmation_callback

    def set_confirmation_callback(self, callback: Callable[[UserConfirmationRequest], bool]) -> None:
        """Sets the interactive confirmation callback for Level 2 actions."""
        self.confirmation_callback = callback

    def check_clearance(self, task: Task) -> bool:
        """
        Evaluates clearance for a given task.
        - Level 0 & Level 1: Approved automatically.
        - Level 2: Requires explicit user confirmation via callback.
        """
        logger.info(
            f"Checking security clearance for action '{task.capability_name}.{task.action_name}' "
            f"[Security Level: {task.security_level.name}]"
        )

        if task.security_level in (SecurityLevel.LEVEL_0, SecurityLevel.LEVEL_1):
            return True

        if task.security_level == SecurityLevel.LEVEL_2:
            req = UserConfirmationRequest(
                task_id=task.task_id,
                capability_name=task.capability_name,
                action_name=task.action_name,
                description=f"Action '{task.capability_name}.{task.action_name}' requires Level 2 approval."
            )
            if self.confirmation_callback:
                approved = self.confirmation_callback(req)
                if approved:
                    logger.info(f"User approved Level 2 action: {task.capability_name}.{task.action_name}")
                    return True
                else:
                    logger.warning(f"User denied Level 2 action: {task.capability_name}.{task.action_name}")
                    return False
            else:
                logger.warning(
                    f"Level 2 action '{task.capability_name}.{task.action_name}' rejected: "
                    f"No user confirmation callback registered."
                )
                return False

        return False
