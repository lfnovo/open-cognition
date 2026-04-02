from fastmcp import FastMCP

import open_cognition.config  # noqa: F401 - loads .env

mcp = FastMCP("open-cognition", instructions="Learning system with spaced repetition. Use the tools to manage topics, flashcards, resources, artifacts, and study sessions.")

# Import tools to register them
import open_cognition.mcp.tools.artifact_tools  # noqa: F401
import open_cognition.mcp.tools.doubt_tools  # noqa: F401
import open_cognition.mcp.tools.flashcard_tools  # noqa: F401
import open_cognition.mcp.tools.resource_tools  # noqa: F401
import open_cognition.mcp.tools.session_tools  # noqa: F401
import open_cognition.mcp.tools.topic_tools  # noqa: F401


def run_mcp():
    import asyncio

    from loguru import logger
    from surreal_basics.migrate import AsyncMigrationRunner

    from open_cognition.config import ensure_data_dir, get_migrations_dir, setup_surreal_defaults

    async def _run_migrations():
        ensure_data_dir()
        setup_surreal_defaults()
        migrations_dir = get_migrations_dir()
        runner = AsyncMigrationRunner(migrations_dir)
        applied = await runner.run_up()
        for m in applied:
            logger.info(f"Applied migration {m.version:03d}_{m.name}")

    asyncio.run(_run_migrations())
    mcp.run()
