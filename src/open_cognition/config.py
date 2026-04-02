import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# App settings
OC_HOST = os.getenv("OC_HOST", "0.0.0.0")
OC_PORT = int(os.getenv("OC_PORT", "8080"))
OC_DATA_DIR = Path(os.getenv("OC_DATA_DIR", os.path.expanduser("~/.open-cognition")))


def ensure_data_dir() -> Path:
    """Create data directory if it doesn't exist. Returns the path."""
    OC_DATA_DIR.mkdir(parents=True, exist_ok=True)
    return OC_DATA_DIR


def setup_surreal_defaults():
    """Set SurrealDB defaults for embedded mode if no connection is configured."""
    # If user already set SURREAL_URL or SURREAL_MODE, respect their choice
    if os.getenv("SURREAL_URL") or os.getenv("SURREAL_MODE"):
        return

    # Default to embedded mode with file in data dir
    ensure_data_dir()
    db_path = str(OC_DATA_DIR / "data.db")
    os.environ.setdefault("SURREAL_MODE", "embedded")
    os.environ.setdefault("SURREAL_PATH", db_path)
    os.environ.setdefault("SURREAL_NAMESPACE", "open_cognition")
    os.environ.setdefault("SURREAL_DATABASE", "main")


def get_connection_info() -> dict:
    """Return current SurrealDB connection info for status display."""
    mode = os.getenv("SURREAL_MODE", "")
    url = os.getenv("SURREAL_URL", "")
    path = os.getenv("SURREAL_PATH", "")
    ns = os.getenv("SURREAL_NS") or os.getenv("SURREAL_NAMESPACE", "")
    db = os.getenv("SURREAL_DB") or os.getenv("SURREAL_DATABASE", "")

    if url:
        if url.startswith("file://"):
            return {"mode": "embedded", "path": url[7:], "namespace": ns, "database": db}
        return {"mode": "remote", "url": url, "namespace": ns, "database": db}
    if mode == "embedded":
        return {"mode": "embedded", "path": path or str(OC_DATA_DIR / "data.db"), "namespace": ns, "database": db}
    if mode == "memory":
        return {"mode": "memory", "namespace": ns, "database": db}
    return {"mode": "embedded (default)", "path": str(OC_DATA_DIR / "data.db"), "namespace": ns, "database": db}


def get_migrations_dir() -> str:
    """Get migrations directory — from package if installed, or local ./migrations."""
    try:
        from importlib.resources import files

        pkg_migrations = files("open_cognition") / "migrations"
        if pkg_migrations.is_dir():
            return str(pkg_migrations)
    except Exception:
        pass

    local = Path("./migrations")
    if local.is_dir():
        return str(local)

    return str(OC_DATA_DIR / "migrations")


def get_templates_dir() -> str:
    """Get templates directory — from package if installed, or local."""
    try:
        from importlib.resources import files

        pkg_templates = files("open_cognition") / "frontend" / "templates"
        if pkg_templates.is_dir():
            return str(pkg_templates)
    except Exception:
        pass

    return "src/open_cognition/frontend/templates"
