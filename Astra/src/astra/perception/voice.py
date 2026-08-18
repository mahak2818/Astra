"""
Voice perception input module (STT Abstraction).
Perception layer passes recognized voice inputs to the Brain.
Perception NEVER invokes Capabilities directly.
"""

from typing import Optional
from astra.utils.logging import setup_logger

logger = setup_logger("astra.perception.voice")


class VoicePerception:
    """STT abstraction for processing voice inputs into recognized text strings."""

    def __init__(self, stt_engine: Optional[Any] = None):
        self.stt_engine = stt_engine

    def process_audio(self, audio_data: bytes) -> str:
        """Converts raw audio bytes into recognized text."""
        logger.info(f"Processing audio input ({len(audio_data)} bytes)...")
        if self.stt_engine:
            return self.stt_engine.transcribe(audio_data)
        # Default mock transcript when external STT library is omitted
        return "open browser and search for Astra Personal AI"
