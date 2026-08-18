"""
Base Capability Interface and Capability Registry for Astra.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type
from astra.models.schemas import CapabilityResult
from astra.utils.logging import setup_logger

logger = setup_logger("astra.capabilities.base")


class Capability(ABC):
    """Abstract base class for all Astra capabilities."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Returns unique capability name."""
        pass

    @abstractmethod
    def execute(self, action: str, parameters: Dict[str, Any]) -> CapabilityResult:
        """Executes named action with given parameters."""
        pass


class CapabilityRegistry:
    """Registry holding all initialized capabilities."""

    def __init__(self) -> None:
        self._capabilities: Dict[str, Capability] = {}

    def register(self, capability: Capability) -> None:
        """Registers capability instance."""
        self._capabilities[capability.name] = capability
        logger.info(f"Registered capability: '{capability.name}'")

    def get(self, name: str) -> Optional[Capability]:
        """Retrieves capability by name."""
        return self._capabilities.get(name)

    def list_all(self) -> Dict[str, Capability]:
        """Lists registered capabilities."""
        return self._capabilities.copy()
