"""
Model Router for Astra Brain. Selects suitable AI model provider or local engine.
"""

from typing import Dict, Any
from astra.config.config import get_config
from astra.utils.logging import setup_logger

logger = setup_logger("astra.brain.model_router")


class ModelRouter:
    """Routes execution or reasoning requests to designated AI models or local engines."""

    def __init__(self) -> None:
        self.config = get_config()

    def route_task(self, domain: str, complexity: str = "normal") -> str:
        """Determines target model string based on domain and complexity."""
        if complexity == "high":
            model = "cloud-reasoning-v1"
        elif domain in ("linux", "git", "files", "terminal"):
            model = "local-deterministic-v1"
        else:
            model = self.config.default_model

        logger.info(f"Routed domain '{domain}' [complexity={complexity}] to model '{model}'")
        return model
