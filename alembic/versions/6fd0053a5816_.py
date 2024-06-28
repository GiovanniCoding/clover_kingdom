"""empty message

Revision ID: 6fd0053a5816
Revises:
Create Date: 2024-06-28 07:54:08.667069

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6fd0053a5816"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "students",
        sa.Column("identification", sa.String(length=10), nullable=False),
        sa.Column("name", sa.String(length=20), nullable=False),
        sa.Column("last_name", sa.String(length=20), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column(
            "magic_affinity",
            sa.Enum(
                "Oscuridad",
                "Luz",
                "Fuego",
                "Agua",
                "Viento",
                "Tierra",
                name="magic_affinity",
            ),
            nullable=False,
        ),
        sa.Column(
            "grimoire",
            sa.Enum(
                "Una Hoja",
                "Dos Hojas",
                "Tres Hojas",
                "Cuatro Hojas",
                "Cinco Hojas",
                name="grimoire_rarity",
            ),
            nullable=True,
        ),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("identification"),
    )
    op.create_table(
        "applications",
        sa.Column(
            "status",
            sa.Enum("Pendiente", "Aprobada", "Rechazada", name="applications_status"),
            nullable=False,
        ),
        sa.Column("student_id", sa.UUID(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["student_id"],
            ["students.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("applications")
    op.drop_table("students")
    # ### end Alembic commands ###
