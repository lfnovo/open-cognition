"""open-cognition CLI — unified entry point for serve and mcp."""

import sys


def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    command = sys.argv[1]

    if command == "serve":
        cmd_serve()
    elif command == "mcp":
        cmd_mcp()
    elif command in ("-h", "--help", "help"):
        print_help()
    elif command == "--version":
        print_version()
    else:
        print(f"Unknown command: {command}")
        print_help()
        sys.exit(1)


def cmd_serve():
    """Start the web application."""
    import os

    from dotenv import load_dotenv

    load_dotenv()

    # Allow CLI overrides: open-cognition serve --port 9090
    args = sys.argv[2:]
    port = None
    host = None
    i = 0
    while i < len(args):
        if args[i] == "--port" and i + 1 < len(args):
            port = int(args[i + 1])
            i += 2
        elif args[i] == "--host" and i + 1 < len(args):
            host = args[i + 1]
            i += 2
        else:
            i += 1

    from open_cognition.config import OC_HOST, OC_PORT

    host = host or OC_HOST
    port = port or OC_PORT

    import uvicorn

    print(f"Starting open-cognition on http://{host}:{port}")
    uvicorn.run("open_cognition.main:app", host=host, port=port, reload=False)


def cmd_mcp():
    """Start the MCP server (stdio mode for Claude Desktop/Code)."""
    from dotenv import load_dotenv

    load_dotenv()

    from open_cognition.mcp.server import mcp

    mcp.run()


def print_help():
    print("""open-cognition — AI-powered learning with spaced repetition

Usage:
  open-cognition serve [--host HOST] [--port PORT]   Start the web app
  open-cognition mcp                                  Start the MCP server
  open-cognition --version                            Show version
  open-cognition --help                               Show this help

Environment variables:
  OC_HOST          Web server host (default: 0.0.0.0)
  OC_PORT          Web server port (default: 8080)
  OC_DATA_DIR      Data directory (default: ~/.open-cognition)
  SURREAL_URL      SurrealDB connection URL
  SURREAL_USER     SurrealDB username (default: root)
  SURREAL_PASSWORD  SurrealDB password (default: root)
  SURREAL_NAMESPACE SurrealDB namespace (default: open-cognition)
  SURREAL_DATABASE  SurrealDB database (default: test)
""")


def print_version():
    from open_cognition import __version__

    print(f"open-cognition {__version__}")


if __name__ == "__main__":
    main()
