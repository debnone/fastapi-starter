"""Add more colums to posts table

Revision ID: 76377c88085c
Revises: b549cd12a5da
Create Date: 2021-11-20 07:19:34.734440

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "76377c88085c"
down_revision = "b549cd12a5da"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )
    pass


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
