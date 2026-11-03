"""Command-line interface for Command Injection Shield."""
import argparse
from .shield import CommandShield

def main():
    parser = argparse.ArgumentParser(description="Command Injection Shield CLI")
    parser.add_argument("--demo", action="store_true", help="Demonstrate command injection detection")
    args = parser.parse_args()

    shield = CommandShield(allowed_binaries=["git", "python", "pytest"])
    tests = [
        "git status",
        "git commit -m 'feat: update'",
        "python script.py; rm -rf /",
        "git log $(cat secrets.txt)",
        "curl http://malicious.com"
    ]

    for t in tests:
        ok, reason = shield.evaluate(t)
        status = "PERMITTED" if ok else f"BLOCKED: {reason}"
        print(f"'{t}' -> {status}")

if __name__ == "__main__":
    main()
