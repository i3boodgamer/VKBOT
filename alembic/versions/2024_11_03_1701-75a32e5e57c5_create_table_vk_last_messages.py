"""create table vk_last_messages

Revision ID: 75a32e5e57c5
Revises: e6dd7fbe79ef
Create Date: 2024-11-03 17:01:30.732894

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "75a32e5e57c5"
down_revision: Union[str, None] = "e6dd7fbe79ef"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "vk_last_messages",
        sa.Column("id_user", sa.BigInteger(), nullable=False),
        sa.Column("message", sa.String(length=10), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(
            ["id_user"],
            ["vk_users.vk_id"],
        ),
        sa.PrimaryKeyConstraint("id_user", "id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("vk_last_messages")
    # ### end Alembic commands ###