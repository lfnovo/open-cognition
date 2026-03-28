"""Convenience entrypoint — runs 'open-cognition serve'."""
import sys

if __name__ == "__main__":
    sys.argv = ["open-cognition", "serve"]
    from open_cognition.cli import main

    main()
