"""
Unit tests for 5 Memory Tiers in MemoryManager.
"""

import tempfile
import unittest
from pathlib import Path

from astra.memory.memory_manager import MemoryManager


class TestMemory(unittest.TestCase):
    def test_memory_tiers(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = Path(tmp_dir) / "test_mem.db"
            mem = MemoryManager(db_path=db_path)

            # 1. Profile Memory
            mem.set_profile("favorite_editor", "VS Code")
            self.assertEqual(mem.get_profile("favorite_editor"), "VS Code")

            # 2. Working Memory
            mem.add_working_context("current_task", "Refactoring")
            self.assertEqual(mem.get_working_context("current_task"), "Refactoring")
            mem.clear_working_memory()
            self.assertIsNone(mem.get_working_context("current_task"))

            # 3. Project Memory
            mem.update_project_progress("Astra", {"phase": 3, "completed": True})
            proj = mem.get_project_progress("Astra")
            self.assertEqual(proj["phase"], 3)

            # 4. Long-term Memory
            mem.remember("python_rule", "Use type hints always")
            self.assertEqual(mem.recall("python_rule"), "Use type hints always")

            # 5. Execution Memory
            mem.record_execution("browser.open", {"status": "ok"})
            exec_history = mem.get_execution_history(limit=5)
            self.assertEqual(len(exec_history), 1)
            self.assertEqual(exec_history[0].content["action"], "browser.open")


if __name__ == "__main__":
    unittest.main()
