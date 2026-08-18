"""
Unit & integration tests for Astra Runtime (Lifecycle, Service Registry, Configuration, Engine).
"""

import asyncio
import tempfile
import unittest
from pathlib import Path

from astra.config.config import AstraConfig, reset_config
from astra.runtime.service_registry import ServiceRegistry
from astra.runtime.lifecycle import LifecycleManager
from astra.runtime.engine import AstraEngine


class TestRuntime(unittest.TestCase):
    def test_config_singleton(self):
        reset_config()
        cfg1 = AstraConfig()
        self.assertEqual(cfg1.app_name, "Astra")
        self.assertTrue(cfg1.data_dir.exists())

    def test_service_registry(self):
        registry = ServiceRegistry()
        registry.register_named("test_service", "hello_world")
        self.assertEqual(registry.resolve_named("test_service"), "hello_world")

        with self.assertRaises(KeyError):
            registry.resolve_named("non_existent")

    def test_lifecycle_manager(self):
        registry = ServiceRegistry()
        lifecycle = LifecycleManager(registry)

        started = []
        stopped = []

        async def run_lifecycle():
            def on_start():
                started.append(True)

            def on_stop():
                stopped.append(True)

            lifecycle.on_startup(on_start)
            lifecycle.on_shutdown(on_stop)

            await lifecycle.startup()
            self.assertTrue(lifecycle.is_running)
            self.assertEqual(started, [True])

            await lifecycle.shutdown()
            self.assertFalse(lifecycle.is_running)
            self.assertEqual(stopped, [True])

        asyncio.run(run_lifecycle())

    def test_astra_engine_execution(self):
        engine = AstraEngine(confirmation_callback=lambda req: True)
        res = engine.execute_request("open browser and search for pytest")
        self.assertEqual(res["domain"], "browser")
        self.assertEqual(res["action"], "search")
        self.assertEqual(len(res["task_results"]), 2)
        self.assertEqual(res["task_results"][1]["status"], "SUCCESS")


if __name__ == "__main__":
    unittest.main()
