"""Add user table

Revision ID: afcac4fe12be
Revises: 3cad37b28a6f
Create Date: 2021-11-20 06:38:46.096805

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "afcac4fe12be"
down_revision = "3cad37b28a6f"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("email", sa.String(), nullable=False, unique=True),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("validate_email_code", sa.String(), nullable=True),
        sa.Column("verify_email", sa.Boolean(), server_default="False", default=False),
        sa.Column("verify_code", sa.Boolean(), server_default="False", default=False),
        sa.Column("reset_password_code", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )
    pass


def downgrade():
    op.drop_table("users")
    pass
