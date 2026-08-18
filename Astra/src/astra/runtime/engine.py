"""
Astra Main Runtime Engine coordinating Perception, Brain, Security, Capabilities, and Memory.
"""

from typing import Any, Dict, List, Optional, Callable
from astra.brain.context import ContextEngine
from astra.brain.intent import IntentEngine
from astra.brain.model_router import ModelRouter
from astra.brain.planner import Planner
from astra.capabilities.base import CapabilityRegistry
from astra.capabilities.browser import BrowserCapability
from astra.capabilities.files import FilesCapability
from astra.capabilities.git import GitCapability
from astra.capabilities.ide import IDECapability
from astra.capabilities.linux import LinuxCapability
from astra.capabilities.terminal import TerminalCapability
from astra.memory.memory_manager import MemoryManager
from astra.models.schemas import ExecutionPlan, Intent, TaskStatus, UserConfirmationRequest
from astra.perception.text import TextPerception
from astra.runtime.lifecycle import LifecycleManager
from astra.runtime.service_registry import ServiceRegistry
from astra.security.gate import SecurityGate
from astra.utils.logging import setup_logger

logger = setup_logger("astra.runtime.engine")


class AstraEngine:
    """
    Main Astra Personal AI Operating Runtime Engine.
    Enforces pipeline: Perception -> Brain (Intent -> Context -> Planner -> Model Router) -> Security Gate -> Capabilities -> Memory.
    """

    def __init__(self, confirmation_callback: Optional[Callable[[UserConfirmationRequest], bool]] = None):
        self.registry = ServiceRegistry()
        self.lifecycle = LifecycleManager(self.registry)

        # 1. Memory Subsystem
        self.memory_manager = MemoryManager()
        self.registry.register(MemoryManager, self.memory_manager)

        # 2. Perception & Security
        self.text_perception = TextPerception()
        self.security_gate = SecurityGate(confirmation_callback=confirmation_callback)

        # 3. Brain Subsystem
        self.intent_engine = IntentEngine()
        self.context_engine = ContextEngine(self.memory_manager)
        self.planner = Planner()
        self.model_router = ModelRouter()

        # 4. Capabilities Subsystem
        self.capability_registry = CapabilityRegistry()
        self._register_default_capabilities()

        logger.info("Astra Engine initialized successfully.")

    def _register_default_capabilities(self) -> None:
        self.capability_registry.register(BrowserCapability())
        self.capability_registry.register(GitCapability())
        self.capability_registry.register(LinuxCapability())
        self.capability_registry.register(FilesCapability())
        self.capability_registry.register(TerminalCapability())
        self.capability_registry.register(IDECapability())

    def execute_request(self, raw_user_input: str) -> Dict[str, Any]:
        """
        Main execution flow:
        1. Perception: Process input text/voice
        2. Brain: Intent -> Context -> Model Router -> Execution Plan
        3. Security Gate: Validate clearance (Level 0, 1, 2)
        4. Capabilities: Execute tasks in DAG plan
        5. Memory: Store interaction into working & execution memory
        """
        logger.info(f"--- Processing user request: '{raw_user_input}' ---")

        # 1. Perception
        perceived_text = self.text_perception.process_text(raw_user_input)

        # 2. Brain
        intent: Intent = self.intent_engine.parse(perceived_text)
        context: Dict[str, Any] = self.context_engine.assemble_context(perceived_text)
        model_name: str = self.model_router.route_task(domain=intent.domain)
        plan: ExecutionPlan = self.planner.create_plan(intent=intent, context=context)

        results: List[Dict[str, Any]] = []

        # 3 & 4. Security & Capabilities Execution
        for task in plan.tasks:
            logger.info(f"Processing Task '{task.task_id}': {task.capability_name}.{task.action_name}")

            # Security clearance check
            if not self.security_gate.check_clearance(task):
                task.status = TaskStatus.FAILED
                task.error = f"Security clearance denied for level {task.security_level.name}"
                results.append({"task_id": task.task_id, "status": "DENIED", "error": task.error})
                logger.warning(f"Task '{task.task_id}' security clearance denied!")
                continue

            cap = self.capability_registry.get(task.capability_name)
            if cap:
                task.status = TaskStatus.RUNNING
                res = cap.execute(task.action_name, task.parameters)
                if res.success:
                    task.status = TaskStatus.COMPLETED
                    task.result = res.data
                    results.append({"task_id": task.task_id, "status": "SUCCESS", "data": res.data})
                else:
                    task.status = TaskStatus.FAILED
                    task.error = res.error
                    results.append({"task_id": task.task_id, "status": "FAILED", "error": res.error})
            else:
                # Fallback handler for general response tasks
                task.status = TaskStatus.COMPLETED
                task.result = {"response": f"Processed intent query: '{intent.raw_input}'"}
                results.append({"task_id": task.task_id, "status": "SUCCESS", "data": task.result})

        # 5. Memory persistence
        self.memory_manager.add_working_context(key=intent.intent_id, value={"input": raw_user_input, "plan": plan.plan_id})
        self.memory_manager.record_execution(action_name=f"{intent.domain}.{intent.action}", result={"results": results})

        return {
            "intent_id": intent.intent_id,
            "domain": intent.domain,
            "action": intent.action,
            "model_used": model_name,
            "task_results": results
        }
