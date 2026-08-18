"""
Unit tests for all registered Capabilities (Browser, Git, Linux, Files, Terminal, IDE).
"""

import tempfile
import unittest
from pathlib import Path

from astra.capabilities.browser import BrowserCapability
from astra.capabilities.git import GitCapability
from astra.capabilities.linux import LinuxCapability
from astra.capabilities.files import FilesCapability
from astra.capabilities.terminal import TerminalCapability
from astra.capabilities.ide import IDECapability


class TestCapabilities(unittest.TestCase):
    def test_browser_capability(self):
        cap = BrowserCapability()
        res = cap.execute("open", {"url": "https://example.com"})
        self.assertTrue(res.success)
        self.assertEqual(res.data["url"], "https://example.com")

    def test_git_capability(self):
        cap = GitCapability()
        res = cap.execute("status", {})
        self.assertTrue(res.success)

    def test_linux_capability(self):
        cap = LinuxCapability()
        res = cap.execute("volume", {"level": "80"})
        self.assertTrue(res.success)
        self.assertEqual(res.data["volume_level"], "80")

    def test_files_capability(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            cap = FilesCapability()
            target_file = Path(tmp_dir) / "sample.txt"

            # Write
            write_res = cap.execute("write_file", {"filepath": str(target_file), "content": "Hello Astra!"})
            self.assertTrue(write_res.success)

            # Read
            read_res = cap.execute("read_file", {"filepath": str(target_file)})
            self.assertTrue(read_res.success)
            self.assertEqual(read_res.data["content"], "Hello Astra!")

            # Delete
            del_res = cap.execute("delete_file", {"filepath": str(target_file)})
            self.assertTrue(del_res.success)
            self.assertFalse(target_file.exists())

    def test_terminal_capability(self):
        cap = TerminalCapability()
        res = cap.execute("execute", {"command": "echo 'Astra Terminal Test'"})
        self.assertTrue(res.success)
        self.assertIn("Astra Terminal Test", res.data["stdout"])

    def test_ide_capability(self):
        cap = IDECapability()
        res = cap.execute("open_project", {"path": "/home/user/project"})
        self.assertTrue(res.success)
        self.assertEqual(res.data["status"], "opened_in_ide")


if __name__ == "__main__":
    unittest.main()
