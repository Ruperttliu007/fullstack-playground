from logging.config import fileConfig
from pathlib import Path
import sys

from alembic import context
from sqlalchemy import engine_from_config, pool

# 读取 alembic.ini
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 让 "src" 可被 import
API_DIR = Path(__file__).resolve().parents[1]   # .../apps/api
if str(API_DIR) not in sys.path:
    sys.path.insert(0, str(API_DIR))            # 这样可以 import src.xxx

from src.models import Base                     # <<— 你的 Base 定义在 src/models.py
target_metadata = Base.metadata                 # <<— 关键：给 Alembic 提供 MetaData

def run_migrations_offline() -> None:
    """在 offline 模式运行迁移（不需要 DB 连接）"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """在 online 模式运行迁移（使用 DB 连接）"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
