"""
Dynamic Plugin Loader for expanding Astra Capabilities at runtime.
"""

import importlib.util
from pathlib import Path
from typing import List, Optional
from astra.capabilities.base import Capability, CapabilityRegistry
from astra.utils.logging import setup_logger

logger = setup_logger("astra.capabilities.plugins")


class PluginManager:
    """Discovers and registers custom capability plugins."""

    def __init__(self, registry: CapabilityRegistry, plugins_dir: Optional[Path] = None):
        self.registry = registry
        self.plugins_dir = plugins_dir or Path.home() / ".astra" / "plugins"
        self.plugins_dir.mkdir(parents=True, exist_ok=True)

    def load_plugins(self) -> List[str]:
        """Scans plugins_dir for .py files and loads custom capability instances."""
        loaded_plugins: List[str] = []
        for file in self.plugins_dir.glob("*.py"):
            if file.name.startswith("_"):
                continue
            try:
                module_name = f"astra_plugin_{file.stem}"
                spec = importlib.util.spec_from_file_location(module_name, file)
                if spec and spec.loader:
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    if hasattr(mod, "get_capability"):
                        cap = mod.get_capability()
                        if isinstance(cap, Capability):
                            self.registry.register(cap)
                            loaded_plugins.append(cap.name)
                            logger.info(f"Loaded dynamic plugin: {cap.name}")
            except Exception as e:
                logger.error(f"Failed to load plugin from {file}: {e}")
        return loaded_plugins
