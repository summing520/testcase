import os

from dotenv import load_dotenv

load_dotenv()


def get_database_query_url() -> str:
    """Primary connection string for external DB introspection (see .env.example)."""
    return (os.environ.get("DB_QUERY_URL") or "").strip()


def get_database_query_schema() -> str | None:
    """Optional PostgreSQL schema (e.g. public). Ignored for SQLite."""
    s = (os.environ.get("DB_QUERY_SCHEMA") or "").strip()
    return s or None
