"""Add foreign-key to posts table

Revision ID: b549cd12a5da
Revises: afcac4fe12be
Create Date: 2021-11-20 07:07:48.332641

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b549cd12a5da"
down_revision = "afcac4fe12be"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade():
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
