"""
System lifecycle manager for Astra Runtime.
"""

from typing import List, Callable, Awaitable, Union
import inspect
from astra.runtime.service_registry import ServiceRegistry
from astra.utils.logging import setup_logger

logger = setup_logger("astra.lifecycle")

LifecycleHook = Union[Callable[[], None], Callable[[], Awaitable[None]]]


class LifecycleManager:
    """Manages application lifecycle: startup sequence, dependency resolution, and graceful shutdown."""

    def __init__(self, registry: ServiceRegistry):
        self.registry = registry
        self._startup_hooks: List[LifecycleHook] = []
        self._shutdown_hooks: List[LifecycleHook] = []
        self.is_running: bool = False

    def on_startup(self, hook: LifecycleHook) -> None:
        """Registers a startup hook."""
        self._startup_hooks.append(hook)

    def on_shutdown(self, hook: LifecycleHook) -> None:
        """Registers a shutdown hook."""
        self._shutdown_hooks.append(hook)

    async def startup(self) -> None:
        """Executes startup sequence."""
        if self.is_running:
            return
        logger.info("Initializing Astra System Lifecycle...")
        for hook in self._startup_hooks:
            if inspect.iscoroutinefunction(hook):
                await hook()  # type: ignore
            else:
                hook()  # type: ignore
        self.is_running = True
        logger.info("Astra System Lifecycle Startup complete.")

    async def shutdown(self) -> None:
        """Executes graceful shutdown sequence in reverse order."""
        if not self.is_running:
            return
        logger.info("Initiating Astra System Graceful Shutdown...")
        for hook in reversed(self._shutdown_hooks):
            try:
                if inspect.iscoroutinefunction(hook):
                    await hook()  # type: ignore
                else:
                    hook()  # type: ignore
            except Exception as e:
                logger.error(f"Error during shutdown hook: {e}")
        self.is_running = False
        logger.info("Astra System Shutdown complete.")
