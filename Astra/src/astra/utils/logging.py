"""
Structured Logging utility for Astra Runtime.
"""

import json
import logging
import sys
from typing import Any, Dict


class JSONFormatter(logging.Formatter):
    """Formats log records as JSON strings."""

    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        if hasattr(record, "extra_data") and isinstance(record.extra_data, dict):
            log_data.update(record.extra_data)
        return json.dumps(log_data)


def setup_logger(name: str = "astra", level: str = "INFO") -> logging.Logger:
    """Configures structured JSON logger."""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)
        logger.propagate = False

    return logger
