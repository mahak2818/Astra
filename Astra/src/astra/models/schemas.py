"""
Core data schemas and type definitions for Astra Runtime.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
import uuid
from typing import Any, Dict, List, Optional


class SecurityLevel(Enum):
    """Security classification levels as defined in docs/08_SECURITY.md."""
    LEVEL_0 = 0  # Low risk (e.g. open apps, web search)
    LEVEL_1 = 1  # Medium risk (e.g. create files, install packages)
    LEVEL_2 = 2  # High risk (e.g. delete files, push git, send emails, spend money) -> Requires confirmation


class TaskStatus(Enum):
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    SKIPPED = auto()
    AWAITING_CONFIRMATION = auto()


@dataclass
class Intent:
    """Parsed user intent."""
    intent_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    raw_input: str = ""
    domain: str = "general"
    action: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Task:
    """Individual execution task within a Plan DAG."""
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    capability_name: str = ""
    action_name: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    security_level: SecurityLevel = SecurityLevel.LEVEL_0
    dependencies: List[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Any] = None
    error: Optional[str] = None


@dataclass
class ExecutionPlan:
    """Deterministic DAG execution plan created by the Brain Planner."""
    plan_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    intent: Intent = field(default_factory=Intent)
    tasks: List[Task] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class MemoryItem:
    """Memory record for memory subsystems."""
    item_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    category: str = "working"  # profile, working, project, long_term, execution
    key: str = ""
    content: Any = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class CapabilityResult:
    """Standardized output from capability actions."""
    success: bool
    data: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UserConfirmationRequest:
    """Request sent when a Level 2 action requires user approval."""
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    task_id: str = ""
    capability_name: str = ""
    action_name: str = ""
    description: str = ""
    security_level: SecurityLevel = SecurityLevel.LEVEL_2
