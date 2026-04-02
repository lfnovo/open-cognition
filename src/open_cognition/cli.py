"""open-cognition CLI — unified entry point for serve, mcp, and status."""

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
    elif command == "status":
        cmd_status()
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
    from dotenv import load_dotenv

    load_dotenv()

    # Allow CLI overrides: open-cognition serve --port 9090
    args = sys.argv[2:]
    port = None
    host = None
    i = 0
    while i < len(args):
        if args[i] == "--port" and i + 1 < len(args):
            try:
                port = int(args[i + 1])
            except ValueError:
                print(f"Error: invalid port '{args[i + 1]}'")
                sys.exit(1)
            i += 2
        elif args[i] == "--host" and i + 1 < len(args):
            host = args[i + 1]
            i += 2
        else:
            i += 1

    from open_cognition.config import OC_HOST, OC_PORT, setup_surreal_defaults

    setup_surreal_defaults()
    host = host or OC_HOST
    port = port or OC_PORT

    import uvicorn

    print(f"Starting open-cognition on http://{host}:{port}")
    uvicorn.run("open_cognition.main:app", host=host, port=port, reload=False)


def cmd_mcp():
    """Start the MCP server (stdio mode for Claude Desktop/Code)."""
    from dotenv import load_dotenv

    load_dotenv()

    from open_cognition.mcp.server import run_mcp

    run_mcp()


def cmd_status():
    """Show connection status and database info."""
    import asyncio

    from dotenv import load_dotenv

    load_dotenv()

    from open_cognition.config import get_connection_info, get_migrations_dir, setup_surreal_defaults

    setup_surreal_defaults()
    info = get_connection_info()

    print("open-cognition status")
    print("=" * 40)
    print(f"  Mode:       {info['mode']}")
    if "path" in info:
        print(f"  DB path:    {info['path']}")
    if "url" in info:
        print(f"  URL:        {info['url']}")
    print(f"  Namespace:  {info['namespace']}")
    print(f"  Database:   {info['database']}")
    print(f"  Migrations: {get_migrations_dir()}")
    print()

    async def _run_checks():
        from surreal_basics import repo_query
        from surreal_basics.migrate import AsyncMigrationRunner

        # Test connection
        print("Testing connection... ", end="", flush=True)
        try:
            await repo_query("RETURN 1")
            print("OK")
        except Exception as e:
            print(f"FAILED\n  Error: {e}")
            return

        # Check migrations
        print("Checking migrations... ", end="", flush=True)
        try:
            runner = AsyncMigrationRunner(get_migrations_dir())
            status = await runner.status()
            applied = len(status.get("applied", []))
            pending = len(status.get("pending", []))
            print(f"{applied} applied, {pending} pending")
        except Exception as e:
            print(f"FAILED\n  Error: {e}")

        # Data summary
        print()
        try:
            counts = {}
            for table in ["topic", "flashcard", "resource", "artifact", "doubt", "review_log", "session_log"]:
                result = await repo_query(f"SELECT count() AS c FROM {table} GROUP ALL")
                counts[table] = result[0]["c"] if result else 0
            print("Data summary:")
            print(f"  Topics:       {counts.get('topic', 0)}")
            print(f"  Flashcards:   {counts.get('flashcard', 0)}")
            print(f"  Resources:    {counts.get('resource', 0)}")
            print(f"  Artifacts:    {counts.get('artifact', 0)}")
            print(f"  Doubts:       {counts.get('doubt', 0)}")
            print(f"  Reviews:      {counts.get('review_log', 0)}")
            print(f"  Sessions:     {counts.get('session_log', 0)}")
        except Exception:
            pass

    asyncio.run(_run_checks())


def print_help():
    print("""open-cognition — AI-powered learning with spaced repetition

Usage:
  open-cognition serve [--host HOST] [--port PORT]   Start the web app
  open-cognition mcp                                  Start the MCP server
  open-cognition status                               Show connection and data status
  open-cognition --version                            Show version
  open-cognition --help                               Show this help

Environment variables:
  OC_HOST            Web server host (default: 0.0.0.0)
  OC_PORT            Web server port (default: 8080)
  OC_DATA_DIR        Data directory (default: ~/.open-cognition)
  SURREAL_URL        SurrealDB connection URL (default: embedded file)
  SURREAL_MODE       Connection mode: embedded, memory, ws, http (default: embedded)
  SURREAL_PATH       Database file path for embedded mode (default: ~/.open-cognition/data.db)
  SURREAL_USER       SurrealDB username (default: root)
  SURREAL_PASSWORD   SurrealDB password (default: root)
  SURREAL_NAMESPACE  SurrealDB namespace (default: open_cognition)
  SURREAL_DATABASE   SurrealDB database (default: main)
""")


def print_version():
    from open_cognition import __version__

    print(f"open-cognition {__version__}")


if __name__ == "__main__":
    main()
