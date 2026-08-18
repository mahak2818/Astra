"""
Unit tests for Plugin Manager dynamic capability loader.
"""

import tempfile
import unittest
from pathlib import Path

from astra.capabilities.base import CapabilityRegistry, Capability
from astra.capabilities.plugins import PluginManager
from astra.models.schemas import CapabilityResult


class DummyPluginCapability(Capability):
    @property
    def name(self) -> str:
        return "custom_plugin"

    def execute(self, action: str, parameters: dict) -> CapabilityResult:
        return CapabilityResult(success=True, data={"plugin": "active"})


class TestPlugins(unittest.TestCase):
    def test_plugin_manager(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            plugins_dir = Path(tmp_dir) / "plugins"
            plugins_dir.mkdir()

            plugin_code = """
from astra.capabilities.base import Capability
from astra.models.schemas import CapabilityResult

class DynamicPlugin(Capability):
    @property
    def name(self):
        return "dynamic_test"

    def execute(self, action, parameters):
        return CapabilityResult(success=True, data="dynamic")

def get_capability():
    return DynamicPlugin()
"""
            (plugins_dir / "test_plugin.py").write_text(plugin_code, encoding="utf-8")

            registry = CapabilityRegistry()
            manager = PluginManager(registry=registry, plugins_dir=plugins_dir)
            loaded = manager.load_plugins()

            self.assertIn("dynamic_test", loaded)
            self.assertIsNotNone(registry.get("dynamic_test"))


if __name__ == "__main__":
    unittest.main()
