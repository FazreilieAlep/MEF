from logging.config import fileConfig
import os
import sys

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# add your model's MetaData object here
from app.core.database import Base
import app.models
import pkgutil
import importlib

def recursive_import(package, exclude_files=None):
    if exclude_files is None:
        exclude_files = []

    package_directory = package.__path__[0]
    for finder, name, is_pkg in pkgutil.iter_modules([package_directory]):
        if name in exclude_files:
            continue
        
        full_name = package.__name__ + '.' + name
        importlib.import_module(full_name)
        if is_pkg:
            recursive_import(importlib.import_module(full_name), exclude_files)

# Import all models from the models package excluding specified files
import app.models
recursive_import(app.models, exclude_files=['crud', 'schema', '__init__', 'associations'])

target_metadata = Base.metadata

# Database URL
config.set_main_option('sqlalchemy.url', 'postgresql+psycopg2://postgres:123456789Abc@localhost:5432/MEF_DB')


# alembic utils
from alembic_utils.pg_function import PGFunction
from alembic_utils.replaceable_entity import register_entities


to_upper = PGFunction(
  schema='public',
  signature='to_upper(some_text text)',
  definition="""
  RETURNS text as
  $$
    SELECT upper(some_text)
  $$ language SQL;
  """
)

register_entities([to_upper])

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
