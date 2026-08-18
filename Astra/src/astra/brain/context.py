"""
Context Engine for aggregating conversation context, system state, and active memory.
"""

from typing import Any, Dict
from astra.memory.memory_manager import MemoryManager
from astra.utils.logging import setup_logger

logger = setup_logger("astra.brain.context")


class ContextEngine:
    """Aggregates memory context for reasoning."""

    def __init__(self, memory_manager: MemoryManager):
        self.memory_manager = memory_manager

    def assemble_context(self, current_intent_text: str) -> Dict[str, Any]:
        """Assembles unified context dictionary from memory tiers."""
        profile_user = self.memory_manager.get_profile("user_name") or "User"
        active_project = self.memory_manager.get_working_context("active_project")
        history = self.memory_manager.list_memories(category="working", limit=5)

        logger.info(f"Assembling context for intent: '{current_intent_text}'")

        return {
            "user": profile_user,
            "active_project": active_project,
            "recent_conversation": [h.content for h in history],
            "query": current_intent_text
        }
