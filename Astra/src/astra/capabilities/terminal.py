"""
Terminal capability implementation.
Actions: execute
"""

import subprocess
from typing import Any, Dict
from astra.capabilities.base import Capability
from astra.models.schemas import CapabilityResult
from astra.utils.logging import setup_logger

logger = setup_logger("astra.capabilities.terminal")


class TerminalCapability(Capability):
    """Executes shell commands."""

    @property
    def name(self) -> str:
        return "terminal"

    def execute(self, action: str, parameters: Dict[str, Any]) -> CapabilityResult:
        logger.info(f"Executing Terminal capability: action='{action}', params={parameters}")

        if action in ("execute", "run_command"):
            command = parameters.get("command", "")
            if not command:
                return CapabilityResult(success=False, error="No command provided")

            try:
                res = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30,
                    check=False
                )
                return CapabilityResult(
                    success=res.returncode == 0,
                    data={
                        "command": command,
                        "exit_code": res.returncode,
                        "stdout": res.stdout,
                        "stderr": res.stderr
                    }
                )
            except Exception as e:
                return CapabilityResult(success=False, error=str(e))

        return CapabilityResult(success=False, error=f"Unknown terminal action: '{action}'")
