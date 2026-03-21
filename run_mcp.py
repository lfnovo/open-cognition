"""Convenience entrypoint — runs 'open-cognition mcp'."""
import sys

sys.argv = ["open-cognition", "mcp"]
from open_cognition.cli import main

main()
