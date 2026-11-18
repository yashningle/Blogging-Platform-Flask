
"""Add user relationship to posts

Revision ID: d82a404c94e1
"""

from alembic import op
import sqlalchemy as sa

revision = "d82a404c94e1"
down_revision = "c98234569a24"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("post", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("user_id", sa.Integer(), nullable=True)
        )

        batch_op.create_foreign_key(
            "fk_post_user_id_user",
            "user",
            ["user_id"],
            ["id"]
        )


def downgrade():
    with op.batch_alter_table("post", schema=None) as batch_op:
        batch_op.drop_constraint(
            "fk_post_user_id_user",
            type_="foreignkey"
        )

        batch_op.drop_column("user_id")
