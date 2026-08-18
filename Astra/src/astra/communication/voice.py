"""
Voice communication module (TTS Abstraction).
"""

from typing import Optional, Any
from astra.utils.logging import setup_logger

logger = setup_logger("astra.communication.voice")


class VoiceOutput:
    """TTS abstraction for speaking responses."""

    def __init__(self, tts_engine: Optional[Any] = None):
        self.tts_engine = tts_engine

    def speak(self, text: str) -> bool:
        logger.info(f"Speaking voice response: '{text}'")
        if self.tts_engine:
            self.tts_engine.say(text)
        return True
