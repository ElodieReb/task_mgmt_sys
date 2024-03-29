"""empty message

Revision ID: adc28fac1c16
Revises: e809a3d26002
Create Date: 2024-01-11 09:46:59.023041

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'adc28fac1c16'
down_revision = 'e809a3d26002'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_by_user', sa.Integer(), nullable=False))
        batch_op.drop_constraint('tasks_user_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['created_by_user'], ['id'])
        batch_op.drop_column('user_id')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)

    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('tasks_user_id_fkey', 'users', ['user_id'], ['id'])
        batch_op.drop_column('created_by_user')

    # ### end Alembic commands ###
