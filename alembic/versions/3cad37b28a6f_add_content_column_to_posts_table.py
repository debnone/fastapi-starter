"""add content column to posts table

Revision ID: 3cad37b28a6f
Revises: 767b94820188
Create Date: 2021-11-20 06:32:15.567137

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3cad37b28a6f"
down_revision = "767b94820188"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
