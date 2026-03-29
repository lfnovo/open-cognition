from typing import Any


def strip_table_prefix(record_id: str) -> str:
    """Strip 'table:' prefix from a SurrealDB record ID for clean API responses."""
    if ":" in str(record_id):
        return str(record_id).split(":", 1)[1]
    return str(record_id)


def ensure_dict(result: Any) -> dict:
    """Ensure a surreal-basics result is a single dict (handles list wrapping)."""
    if isinstance(result, list):
        return result[0]
    return result


def ensure_list(result: Any) -> list[dict]:
    """Ensure a surreal-basics result is a list."""
    if isinstance(result, dict):
        return [result]
    return result
