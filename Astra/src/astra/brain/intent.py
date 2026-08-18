"""
Intent Engine for Astra Brain Subsystem.
Parses natural language queries into structured Intents and actions.
"""

from typing import Dict, Any, List
from astra.models.schemas import Intent
from astra.utils.logging import setup_logger

logger = setup_logger("astra.brain.intent")


class IntentEngine:
    """Parses user requests into structured Intent objects."""

    def __init__(self) -> None:
        pass

    def parse(self, raw_input: str) -> Intent:
        """Parses raw text/voice string into Intent."""
        text = raw_input.strip()
        lower_text = text.lower()

        logger.info(f"Parsing intent for input: '{text}'")

        # Rules-based deterministic pattern matching for primary domains
        if lower_text.startswith("open browser") or lower_text.startswith("search web") or lower_text.startswith("search for") or lower_text.startswith("search"):
            query = text
            for prefix in ["open browser and search for", "open browser and search", "search web for", "search web", "search for", "open browser"]:
                if query.lower().startswith(prefix):
                    query = query[len(prefix):].strip()
                    break
            return Intent(
                raw_input=raw_input,
                domain="browser",
                action="search",
                parameters={"query": query or text}
            )

        if lower_text.startswith("git status"):
            return Intent(
                raw_input=raw_input,
                domain="git",
                action="status",
                parameters={}
            )

        if lower_text.startswith("git commit"):
            message = text.replace("git commit", "").strip() or "Auto commit by Astra"
            return Intent(
                raw_input=raw_input,
                domain="git",
                action="commit",
                parameters={"message": message}
            )

        if lower_text.startswith("git push"):
            return Intent(
                raw_input=raw_input,
                domain="git",
                action="push",
                parameters={}
            )

        if lower_text.startswith("open app") or lower_text.startswith("launch"):
            app_name = text.replace("open app", "").replace("launch", "").strip()
            return Intent(
                raw_input=raw_input,
                domain="linux",
                action="open_app",
                parameters={"app_name": app_name}
            )

        if lower_text.startswith("set volume"):
            vol = text.replace("set volume", "").replace("%", "").strip()
            return Intent(
                raw_input=raw_input,
                domain="linux",
                action="volume",
                parameters={"level": vol}
            )

        if lower_text.startswith("notify") or lower_text.startswith("send notification"):
            msg = text.replace("send notification", "").replace("notify", "").strip()
            return Intent(
                raw_input=raw_input,
                domain="linux",
                action="notifications",
                parameters={"message": msg}
            )

        if lower_text.startswith("create file") or lower_text.startswith("write file"):
            parts = text.split("with content")
            filepath = parts[0].replace("create file", "").replace("write file", "").strip()
            content = parts[1].strip() if len(parts) > 1 else ""
            return Intent(
                raw_input=raw_input,
                domain="files",
                action="write_file",
                parameters={"filepath": filepath, "content": content}
            )

        if lower_text.startswith("delete file") or lower_text.startswith("remove file"):
            filepath = text.replace("delete file", "").replace("remove file", "").strip()
            return Intent(
                raw_input=raw_input,
                domain="files",
                action="delete_file",
                parameters={"filepath": filepath}
            )

        if lower_text.startswith("run command") or lower_text.startswith("exec"):
            cmd = text.replace("run command", "").replace("exec", "").strip()
            return Intent(
                raw_input=raw_input,
                domain="terminal",
                action="execute",
                parameters={"command": cmd}
            )

        # Fallback general intent
        return Intent(
            raw_input=raw_input,
            domain="general",
            action="query",
            parameters={"text": text}
        )
