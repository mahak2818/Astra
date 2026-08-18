"""
Service Registry for Astra Dependency Injection.
"""

from typing import Any, Dict, Type, TypeVar, Optional

T = TypeVar("T")


class ServiceRegistry:
    """Central container for registered services and singletons."""

    def __init__(self) -> None:
        self._services: Dict[Type[Any], Any] = {}
        self._named_services: Dict[str, Any] = {}

    def register(self, service_type: Type[T], instance: T) -> None:
        """Registers a service by type."""
        self._services[service_type] = instance

    def register_named(self, name: str, instance: Any) -> None:
        """Registers a service by name."""
        self._named_services[name] = instance

    def resolve(self, service_type: Type[T]) -> T:
        """Resolves a service by type."""
        if service_type not in self._services:
            raise KeyError(f"Service of type {service_type.__name__} is not registered.")
        return self._services[service_type]  # type: ignore

    def resolve_named(self, name: str) -> Any:
        """Resolves a service by name."""
        if name not in self._named_services:
            raise KeyError(f"Service named '{name}' is not registered.")
        return self._named_services[name]

    def has(self, service_type: Type[Any]) -> bool:
        """Checks if service type is registered."""
        return service_type in self._services

    def clear(self) -> None:
        """Clears registry."""
        self._services.clear()
        self._named_services.clear()
