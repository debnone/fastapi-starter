"""create post table

Revision ID: 767b94820188
Revises: 
Create Date: 2021-11-20 06:22:19.555240

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "767b94820188"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("title", sa.String, nullable=False),
    )
    pass


def downgrade():
    op.drop_table("posts")
    pass
