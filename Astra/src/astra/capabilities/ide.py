"""
IDE capability implementation.
Actions: open_project
"""

from typing import Any, Dict
from astra.capabilities.base import Capability
from astra.models.schemas import CapabilityResult
from astra.utils.logging import setup_logger

logger = setup_logger("astra.capabilities.ide")


class IDECapability(Capability):
    """IDE integration capability."""

    @property
    def name(self) -> str:
        return "ide"

    def execute(self, action: str, parameters: Dict[str, Any]) -> CapabilityResult:
        logger.info(f"Executing IDE capability: action='{action}', params={parameters}")

        if action == "open_project":
            project_path = parameters.get("path", ".")
            return CapabilityResult(success=True, data={"path": project_path, "status": "opened_in_ide"})

        return CapabilityResult(success=False, error=f"Unknown IDE action: '{action}'")
