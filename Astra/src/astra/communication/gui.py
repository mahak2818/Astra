"""
GUI Communication interface for Astra desktop user output.
"""

from typing import Any, Dict
from astra.utils.logging import setup_logger

logger = setup_logger("astra.communication.gui")


class GUIOutput:
    """Manages visual outputs to user interface."""

    def render_response(self, text: str, data: Optional[Dict[str, Any]] = None) -> None:
        logger.info(f"Rendering GUI response: text='{text}', data={data}")
