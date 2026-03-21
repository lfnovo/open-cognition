"""Convenience entrypoint — runs 'open-cognition serve'."""
import sys

sys.argv = ["open-cognition", "serve"]
from open_cognition.cli import main

main()
