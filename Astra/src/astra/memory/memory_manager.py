"""
Unified Memory Manager for Astra handling 5 distinct memory tiers backed by SQLite.
"""

import json
import sqlite3
from typing import Any, Dict, List, Optional
from pathlib import Path
from datetime import datetime, timezone

from astra.config.config import get_config
from astra.models.schemas import MemoryItem
from astra.utils.logging import setup_logger

logger = setup_logger("astra.memory")


class MemoryManager:
    """
    Coordinates 5 Memory Tiers:
    1. Profile Memory
    2. Working Memory
    3. Project Memory
    4. Long-term Memory
    5. Execution Memory
    """

    def __init__(self, db_path: Optional[Path] = None):
        config = get_config()
        self.db_path = db_path or config.db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(str(self.db_path))

    def _init_db(self) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    item_id TEXT PRIMARY KEY,
                    category TEXT NOT NULL,
                    key TEXT NOT NULL,
                    content TEXT NOT NULL,
                    metadata TEXT,
                    timestamp TEXT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_category_key ON memories (category, key)
            """)
            conn.commit()

    # --- Profile Memory ---
    def set_profile(self, key: str, value: Any) -> None:
        self.save_memory(category="profile", key=key, content=value)

    def get_profile(self, key: str) -> Optional[Any]:
        item = self.get_memory(category="profile", key=key)
        return item.content if item else None

    # --- Working Memory ---
    def add_working_context(self, key: str, value: Any) -> None:
        self.save_memory(category="working", key=key, content=value)

    def get_working_context(self, key: str) -> Optional[Any]:
        item = self.get_memory(category="working", key=key)
        return item.content if item else None

    def clear_working_memory(self) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM memories WHERE category = 'working'")
            conn.commit()

    # --- Project Memory ---
    def update_project_progress(self, project_name: str, progress: Dict[str, Any]) -> None:
        self.save_memory(category="project", key=project_name, content=progress)

    def get_project_progress(self, project_name: str) -> Optional[Dict[str, Any]]:
        item = self.get_memory(category="project", key=project_name)
        return item.content if item else None

    # --- Long-term Memory ---
    def remember(self, key: str, fact: Any, metadata: Optional[Dict[str, Any]] = None) -> None:
        self.save_memory(category="long_term", key=key, content=fact, metadata=metadata)

    def recall(self, key: str) -> Optional[Any]:
        item = self.get_memory(category="long_term", key=key)
        return item.content if item else None

    # --- Execution Memory ---
    def record_execution(self, action_name: str, result: Dict[str, Any]) -> None:
        key = f"exec_{datetime.now(timezone.utc).timestamp()}"
        self.save_memory(category="execution", key=key, content={"action": action_name, "result": result})

    def get_execution_history(self, limit: int = 50) -> List[MemoryItem]:
        return self.list_memories(category="execution", limit=limit)

    # --- Core SQLite Persistence primitives ---
    def save_memory(
        self,
        category: str,
        key: str,
        content: Any,
        metadata: Optional[Dict[str, Any]] = None
    ) -> MemoryItem:
        item = MemoryItem(
            category=category,
            key=key,
            content=content,
            metadata=metadata or {}
        )
        content_json = json.dumps(content)
        metadata_json = json.dumps(item.metadata)
        ts_str = item.timestamp.isoformat()

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO memories (item_id, category, key, content, metadata, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (item.item_id, category, key, content_json, metadata_json, ts_str))
            conn.commit()

        logger.debug(f"Saved memory item: [{category}] {key}")
        return item

    def get_memory(self, category: str, key: str) -> Optional[MemoryItem]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT item_id, category, key, content, metadata, timestamp
                FROM memories
                WHERE category = ? AND key = ?
                ORDER BY timestamp DESC
                LIMIT 1
            """, (category, key))
            row = cursor.fetchone()
            if not row:
                return None
            return MemoryItem(
                item_id=row[0],
                category=row[1],
                key=row[2],
                content=json.loads(row[3]),
                metadata=json.loads(row[4]) if row[4] else {},
                timestamp=datetime.fromisoformat(row[5])
            )

    def list_memories(self, category: str, limit: int = 100) -> List[MemoryItem]:
        items: List[MemoryItem] = []
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT item_id, category, key, content, metadata, timestamp
                FROM memories
                WHERE category = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (category, limit))
            rows = cursor.fetchall()
            for row in rows:
                items.append(MemoryItem(
                    item_id=row[0],
                    category=row[1],
                    key=row[2],
                    content=json.loads(row[3]),
                    metadata=json.loads(row[4]) if row[4] else {},
                    timestamp=datetime.fromisoformat(row[5])
                ))
        return items
