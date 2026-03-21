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
    mcp.run()
