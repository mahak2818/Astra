"""
Centralized Configuration for Astra Runtime.
"""

from dataclasses import dataclass, field
import os
from pathlib import Path
from typing import Optional


@dataclass
class AstraConfig:
    """Central configuration parameters for Astra."""

    app_name: str = "Astra"
    environment: str = field(default_factory=lambda: os.getenv("ASTRA_ENV", "development"))
    log_level: str = field(default_factory=lambda: os.getenv("ASTRA_LOG_LEVEL", "INFO"))
    data_dir: Path = field(
        default_factory=lambda: Path(
            os.getenv("ASTRA_DATA_DIR", str(Path.home() / ".astra"))
        )
    )
    db_path: Path = field(init=False)
    default_model: str = field(
        default_factory=lambda: os.getenv("ASTRA_DEFAULT_MODEL", "astra-deterministic-v1")
    )
    auto_confirm_level1: bool = True

    def __post_init__(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.data_dir / "astra_memory.db"


_config_instance: Optional[AstraConfig] = None


def get_config() -> AstraConfig:
    """Returns singleton configuration instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = AstraConfig()
    return _config_instance


def reset_config() -> AstraConfig:
    """Resets configuration instance (useful for testing)."""
    global _config_instance
    _config_instance = AstraConfig()
    return _config_instance
