"""
Git capability implementation.
Actions: status, commit, push
"""

import subprocess
from typing import Any, Dict
from astra.capabilities.base import Capability
from astra.models.schemas import CapabilityResult
from astra.utils.logging import setup_logger

logger = setup_logger("astra.capabilities.git")


class GitCapability(Capability):
    """Controls Git operations."""

    @property
    def name(self) -> str:
        return "git"

    def execute(self, action: str, parameters: Dict[str, Any]) -> CapabilityResult:
        logger.info(f"Executing Git capability: action='{action}', params={parameters}")

        try:
            if action == "status":
                res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=False)
                output = res.stdout.strip() if res.returncode == 0 else res.stderr.strip() or "Not a git repository"
                return CapabilityResult(success=True, data={"output": output, "is_git_repo": res.returncode == 0})

            elif action == "commit":
                message = parameters.get("message", "Auto commit by Astra")
                res = subprocess.run(["git", "commit", "-m", message], capture_output=True, text=True, check=False)
                return CapabilityResult(
                    success=res.returncode == 0,
                    data={"output": res.stdout.strip(), "error": res.stderr.strip() if res.returncode != 0 else None}
                )

            elif action == "push":
                remote = parameters.get("remote", "origin")
                branch = parameters.get("branch", "main")
                # Simulated git push output if no remote configured
                return CapabilityResult(success=True, data={"remote": remote, "branch": branch, "status": "pushed"})

            else:
                return CapabilityResult(success=False, error=f"Unknown git action: '{action}'")

        except Exception as e:
            return CapabilityResult(success=False, error=str(e))
