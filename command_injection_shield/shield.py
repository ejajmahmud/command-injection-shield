"""Strict shell command tokenization and operator injection guardrail."""
import shlex
from typing import Tuple, List, Set

DANGEROUS_OPERATORS = {";", "&&", "||", "|", "&", ">", "<", ">>", "$(", "`"}


class CommandShield:
    def __init__(self, allowed_binaries: List[str] = None):
        self.allowed_binaries: Set[str] = set(b.lower() for b in (allowed_binaries or ["git", "pytest", "python", "npm", "cargo"]))

    def evaluate(self, command_line: str) -> Tuple[bool, str]:
        # Fast check for subshell syntax
        if "$(" in command_line or "`" in command_line:
            return False, "Command contains forbidden subshell evaluation ('$(' or '`')"

        # Check raw string for forbidden operators before tokenizing
        for op in [";", "&&", "||", "|", ">>", ">"]:
            if op in command_line:
                return False, f"Command contains forbidden chaining/redirection operator '{op}'"

        try:
            tokens = shlex.split(command_line, posix=True)
        except Exception as e:
            return False, f"Malformed shell syntax: {e}"

        if not tokens:
            return False, "Empty command"

        binary = tokens[0].lower()
        # Strip path if provided
        import os
        base_binary = os.path.basename(binary).replace(".exe", "")

        if self.allowed_binaries and base_binary not in self.allowed_binaries:
            return False, f"Binary '{base_binary}' is not in the allowed executable whitelist: {sorted(list(self.allowed_binaries))}"

        return True, "Safe"
