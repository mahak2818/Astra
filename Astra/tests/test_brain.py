"""
Unit tests for Brain Subsystem (Intent, Context, ModelRouter, Planner).
"""

import tempfile
import unittest
from pathlib import Path

from astra.brain.intent import IntentEngine
from astra.brain.context import ContextEngine
from astra.brain.model_router import ModelRouter
from astra.brain.planner import Planner
from astra.memory.memory_manager import MemoryManager
from astra.models.schemas import SecurityLevel


class TestBrain(unittest.TestCase):
    def test_intent_engine(self):
        engine = IntentEngine()

        intent_search = engine.parse("open browser and search for quantum computing")
        self.assertEqual(intent_search.domain, "browser")
        self.assertEqual(intent_search.action, "search")
        self.assertEqual(intent_search.parameters["query"], "quantum computing")

        intent_git = engine.parse("git push")
        self.assertEqual(intent_git.domain, "git")
        self.assertEqual(intent_git.action, "push")

        intent_app = engine.parse("launch firefox")
        self.assertEqual(intent_app.domain, "linux")
        self.assertEqual(intent_app.action, "open_app")

    def test_planner(self):
        planner = Planner()
        engine = IntentEngine()

        intent = engine.parse("delete file /tmp/old.txt")
        context = {}
        plan = planner.create_plan(intent, context)

        self.assertEqual(len(plan.tasks), 1)
        self.assertEqual(plan.tasks[0].capability_name, "files")
        self.assertEqual(plan.tasks[0].action_name, "delete_file")
        self.assertEqual(plan.tasks[0].security_level, SecurityLevel.LEVEL_2)

    def test_context_engine(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = Path(tmp_dir) / "test_context.db"
            mem = MemoryManager(db_path=db_path)
            mem.set_profile("user_name", "Alice")
            mem.add_working_context("active_project", "Astra AI")

            ctx_engine = ContextEngine(mem)
            context = ctx_engine.assemble_context("query test")

            self.assertEqual(context["user"], "Alice")
            self.assertEqual(context["active_project"], "Astra AI")

    def test_model_router(self):
        router = ModelRouter()
        self.assertEqual(router.route_task(domain="git"), "local-deterministic-v1")
        self.assertEqual(router.route_task(domain="general", complexity="high"), "cloud-reasoning-v1")


if __name__ == "__main__":
    unittest.main()
