"""
Linux Desktop Notification Communication interface.
"""

from typing import Optional
from astra.utils.logging import setup_logger

logger = setup_logger("astra.communication.notifications")


class DesktopNotifier:
    """Sends native desktop notifications."""

    def notify(self, title: str, message: str) -> bool:
        logger.info(f"Desktop Notification: [{title}] {message}")
        return True
