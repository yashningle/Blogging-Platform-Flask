
"""Add category model"""

from alembic import op
import sqlalchemy as sa

revision = "e7f8a9b0c1d2"
down_revision = "d82a404c94e1"
branch_labels = None
depends_on = None


def upgrade():

    # Check existing database tables
    inspector = sa.inspect(op.get_bind())
    tables = inspector.get_table_names()

    # Create category table only if it does not exist
    if "category" not in tables:
        op.create_table(
            "category",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("name", sa.String(length=50), nullable=False),
            sa.UniqueConstraint("name", name="uq_category_name")
        )

    # Check existing post columns
    inspector = sa.inspect(op.get_bind())
    columns = [
        column["name"]
        for column in inspector.get_columns("post")
    ]

    if "category_id" not in columns:

        with op.batch_alter_table(
            "post",
            naming_convention={
                "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
                "pk": "pk_%(table_name)s",
                "uq": "uq_%(table_name)s_%(column_0_name)s"
            }
        ) as batch_op:

            batch_op.add_column(
                sa.Column("category_id", sa.Integer(), nullable=True)
            )

            batch_op.create_foreign_key(
                "fk_post_category_id_category",
                "category",
                ["category_id"],
                ["id"]
            )


def downgrade():

    with op.batch_alter_table(
        "post",
        naming_convention={
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s"
        }
    ) as batch_op:

        batch_op.drop_constraint(
            "fk_post_category_id_category",
            type_="foreignkey"
        )

        batch_op.drop_column("category_id")

    op.drop_table("category")
