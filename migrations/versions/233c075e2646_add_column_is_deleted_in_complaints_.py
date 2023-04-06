"""Add column 'is_deleted' in complaints table nullable=False

Revision ID: 233c075e2646
Revises: e4bfaafe9661
Create Date: 2023-04-05 20:47:14.998014

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '233c075e2646'
down_revision = 'e4bfaafe9661'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('complaints', schema=None) as batch_op:
        batch_op.alter_column('is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('complaints', schema=None) as batch_op:
        batch_op.alter_column('is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=True)

    # ### end Alembic commands ###
