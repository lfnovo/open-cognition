"""Convenience entrypoint — runs 'open-cognition mcp'."""
import sys

if __name__ == "__main__":
    sys.argv = ["open-cognition", "mcp"]
    from open_cognition.cli import main

    main()
