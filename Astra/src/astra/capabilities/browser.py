"""
Browser capability implementation.
Actions: open, search, click, type
"""

from typing import Any, Dict
from astra.capabilities.base import Capability
from astra.models.schemas import CapabilityResult
from astra.utils.logging import setup_logger

logger = setup_logger("astra.capabilities.browser")


class BrowserCapability(Capability):
    """Controls browser actions."""

    @property
    def name(self) -> str:
        return "browser"

    def execute(self, action: str, parameters: Dict[str, Any]) -> CapabilityResult:
        logger.info(f"Executing Browser capability: action='{action}', params={parameters}")

        if action == "open":
            url = parameters.get("url", "https://google.com")
            return CapabilityResult(success=True, data={"url": url, "status": "opened"})

        elif action == "search":
            query = parameters.get("query", "")
            return CapabilityResult(
                success=True,
                data={"query": query, "url": f"https://www.google.com/search?q={query}", "status": "searched"}
            )

        elif action == "click":
            selector = parameters.get("selector", "")
            return CapabilityResult(success=True, data={"selector": selector, "status": "clicked"})

        elif action == "type":
            selector = parameters.get("selector", "")
            text = parameters.get("text", "")
            return CapabilityResult(success=True, data={"selector": selector, "text": text, "status": "typed"})

        else:
            return CapabilityResult(success=False, error=f"Unknown browser action: '{action}'")
