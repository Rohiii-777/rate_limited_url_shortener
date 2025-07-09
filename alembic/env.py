from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
from dotenv import load_dotenv
from app.db import Base
from app.models import *  # import all models

load_dotenv()

# Alembic Config object
config = context.config

# Interpret .ini file for logging
fileConfig(config.config_file_name)

# Set SQLAlchemy URL
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

target_metadata = Base.metadata

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # track type changes
        )

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()
