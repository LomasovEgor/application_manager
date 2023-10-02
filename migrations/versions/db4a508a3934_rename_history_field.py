"""rename History field

Revision ID: db4a508a3934
Revises: f4a57453f3bf
Create Date: 2023-10-02 14:36:41.588988

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db4a508a3934'
down_revision: Union[str, None] = 'f4a57453f3bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('history', sa.Column('program_name', sa.String(), nullable=False))
    op.drop_column('history', 'program_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('history', sa.Column('program_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('history', 'program_name')
    # ### end Alembic commands ###