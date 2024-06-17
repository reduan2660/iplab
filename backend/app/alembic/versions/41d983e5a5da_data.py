"""data

Revision ID: 41d983e5a5da
Revises: df4e066db9dc
Create Date: 2024-06-18 02:30:54.103628

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '41d983e5a5da'
down_revision: Union[str, None] = 'df4e066db9dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

from app.config import HASHED_SUPERADMIN_PASSWORD


def upgrade() -> None:
    meta = sa.MetaData()

    users_tbl = sa.Table('users', meta, autoload_with=op.get_bind())
    op.bulk_insert(users_tbl, [
        {"name": "SuperAdmin", "email": "super@admin.com", "password": HASHED_SUPERADMIN_PASSWORD, "is_admin": 1},
    ])

    categories_tbl = sa.Table('categories', meta, autoload_with=op.get_bind())
    op.bulk_insert(categories_tbl, [
        {"name": "Phone", "rating_params": "camera, battery, performance, display, build", "config_params": "display_size, display_res, display_panel, ram, battery_capacity, camera_pixel, max_charge_capacity"},
        {"name": "Laptop", "rating_params": "performance, display, battery, build, keyboard", "config_params": "display_size, display_res, display_panel, ram, battery_capacity, cpu, gpu, storage_type, storage_capacity"},
        {"name": "Tablet", "rating_params": "performance, display, battery, build, camera", "config_params": "display_size, display_res, display_panel, ram, battery_capacity, cpu, gpu, storage_type, storage_capacity"},
    ])

def downgrade() -> None:
    meta = sa.MetaData()

    op.execute("DELETE FROM comments")
    op.execute("DELETE FROM products")
    op.execute("DELETE FROM categories")
    op.execute("DELETE FROM sessions")
    op.execute("DELETE FROM users")

