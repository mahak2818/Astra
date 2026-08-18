"""
Text perception input module.
"""

from typing import Dict, Any
from astra.utils.logging import setup_logger

logger = setup_logger("astra.perception.text")


class TextPerception:
    """Processes textual inputs from CLI, GUI, or external events."""

    def process_text(self, text: str) -> str:
        logger.info(f"Received text perception input: '{text}'")
        return text.strip()
