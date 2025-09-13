from __future__ import annotations
import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# --- Alembic Config
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- Make your package importable when running from alembic/
# Adjust the path one level up (project root)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# --- Import your Flask app and db
from app import create_app, db  # your package name = "app"

app = create_app()

# Use your app's DB URL as the single source of truth
config.set_main_option("sqlalchemy.url", app.config["SQLALCHEMY_DATABASE_URI"])

# Tell Alembic where to find table metadata
target_metadata = db.Model.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    with app.app_context():
        context.configure(
            url=url,
            target_metadata=target_metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
            compare_type=True,              # detect column type changes
            compare_server_default=True,    # detect server_default changes
        )

        with context.begin_transaction():
            context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection, app.app_context():
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            # render_as_batch=True,  # Uncomment if you ever target SQLite and need batch ops
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
