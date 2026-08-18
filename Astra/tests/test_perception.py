"""
Unit tests for Perception (Text, Voice, Vision) and Communication interfaces.
"""

import unittest
from astra.perception.text import TextPerception
from astra.perception.voice import VoicePerception
from astra.perception.vision import VisionPerception
from astra.communication.voice import VoiceOutput
from astra.communication.notifications import DesktopNotifier


class TestPerceptionAndCommunication(unittest.TestCase):
    def test_perception_layers(self):
        text_p = TextPerception()
        self.assertEqual(text_p.process_text("  hello world  "), "hello world")

        voice_p = VoicePerception()
        transcript = voice_p.process_audio(b"audio_bytes")
        self.assertIn("Astra", transcript)

        vision_p = VisionPerception()
        vis_data = vision_p.analyze_image(b"fake_frame")
        self.assertIn("objects_detected", vis_data)

    def test_communication_layers(self):
        voice_out = VoiceOutput()
        self.assertTrue(voice_out.speak("System ready"))

        notifier = DesktopNotifier()
        self.assertTrue(notifier.notify("Astra", "Task complete"))


if __name__ == "__main__":
    unittest.main()
