"""
Brain Planner module for generating deterministic execution DAG plans.
"""

from typing import Dict, Any, List
from astra.models.schemas import ExecutionPlan, Intent, SecurityLevel, Task, TaskStatus
from astra.utils.logging import setup_logger

logger = setup_logger("astra.brain.planner")

SECURITY_MAP: Dict[str, SecurityLevel] = {
    # Level 0 actions
    "browser.open": SecurityLevel.LEVEL_0,
    "browser.search": SecurityLevel.LEVEL_0,
    "linux.open_app": SecurityLevel.LEVEL_0,
    "linux.volume": SecurityLevel.LEVEL_0,
    "linux.notifications": SecurityLevel.LEVEL_0,
    "git.status": SecurityLevel.LEVEL_0,
    "files.read_file": SecurityLevel.LEVEL_0,
    # Level 1 actions
    "files.write_file": SecurityLevel.LEVEL_1,
    "terminal.execute": SecurityLevel.LEVEL_1,
    "git.commit": SecurityLevel.LEVEL_1,
    # Level 2 actions (require explicit user confirmation)
    "files.delete_file": SecurityLevel.LEVEL_2,
    "git.push": SecurityLevel.LEVEL_2,
    "terminal.sudo_execute": SecurityLevel.LEVEL_2,
}


class Planner:
    """Creates deterministic task graph execution plans from intents."""

    def __init__(self) -> None:
        pass

    def get_security_level(self, capability: str, action: str) -> SecurityLevel:
        key = f"{capability}.{action}"
        return SECURITY_MAP.get(key, SecurityLevel.LEVEL_1)

    def create_plan(self, intent: Intent, context: Dict[str, Any]) -> ExecutionPlan:
        """Constructs a deterministic DAG ExecutionPlan for a given intent."""
        plan = ExecutionPlan(intent=intent)
        logger.info(f"Creating execution plan for intent: domain='{intent.domain}', action='{intent.action}'")

        if intent.domain == "browser" and intent.action == "search":
            task1 = Task(
                capability_name="browser",
                action_name="open",
                parameters={"url": "https://google.com"},
                security_level=self.get_security_level("browser", "open")
            )
            task2 = Task(
                capability_name="browser",
                action_name="search",
                parameters={"query": intent.parameters.get("query", "")},
                security_level=self.get_security_level("browser", "search"),
                dependencies=[task1.task_id]
            )
            plan.tasks.extend([task1, task2])

        elif intent.domain == "git" and intent.action == "push":
            task_status = Task(
                capability_name="git",
                action_name="status",
                parameters={},
                security_level=self.get_security_level("git", "status")
            )
            task_push = Task(
                capability_name="git",
                action_name="push",
                parameters={},
                security_level=self.get_security_level("git", "push"),
                dependencies=[task_status.task_id]
            )
            plan.tasks.extend([task_status, task_push])

        elif intent.domain in ("browser", "git", "linux", "files", "terminal"):
            sec_level = self.get_security_level(intent.domain, intent.action)
            task = Task(
                capability_name=intent.domain,
                action_name=intent.action,
                parameters=intent.parameters,
                security_level=sec_level
            )
            plan.tasks.append(task)

        else:
            # General query plan
            task = Task(
                capability_name="general",
                action_name="respond",
                parameters=intent.parameters,
                security_level=SecurityLevel.LEVEL_0
            )
            plan.tasks.append(task)

        return plan
