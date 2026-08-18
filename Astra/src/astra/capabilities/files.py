"""
Files capability implementation.
Actions: read_file, write_file, delete_file
"""

from pathlib import Path
from typing import Any, Dict
from astra.capabilities.base import Capability
from astra.models.schemas import CapabilityResult
from astra.utils.logging import setup_logger

logger = setup_logger("astra.capabilities.files")


class FilesCapability(Capability):
    """File system operations capability."""

    @property
    def name(self) -> str:
        return "files"

    def execute(self, action: str, parameters: Dict[str, Any]) -> CapabilityResult:
        logger.info(f"Executing Files capability: action='{action}', params={parameters}")

        try:
            filepath_str = parameters.get("filepath", "")
            if not filepath_str:
                return CapabilityResult(success=False, error="No filepath provided")

            path = Path(filepath_str)

            if action == "read_file":
                if not path.exists():
                    return CapabilityResult(success=False, error=f"File not found: {path}")
                content = path.read_text(encoding="utf-8")
                return CapabilityResult(success=True, data={"filepath": str(path), "content": content})

            elif action == "write_file":
                path.parent.mkdir(parents=True, exist_ok=True)
                content = parameters.get("content", "")
                path.write_text(content, encoding="utf-8")
                return CapabilityResult(success=True, data={"filepath": str(path), "bytes_written": len(content)})

            elif action == "delete_file":
                if path.exists():
                    path.unlink()
                    return CapabilityResult(success=True, data={"filepath": str(path), "status": "deleted"})
                return CapabilityResult(success=False, error=f"File not found: {path}")

            else:
                return CapabilityResult(success=False, error=f"Unknown files action: '{action}'")

        except Exception as e:
            return CapabilityResult(success=False, error=str(e))
