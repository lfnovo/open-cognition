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


def get_migrations_dir() -> str:
    """Get migrations directory — from package if installed, or local ./migrations."""
    # Try package-bundled migrations first
    try:
        from importlib.resources import files

        pkg_migrations = files("open_cognition") / "migrations"
        if pkg_migrations.is_dir():
            return str(pkg_migrations)
    except Exception:
        pass

    # Fallback to local directory (development mode)
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
