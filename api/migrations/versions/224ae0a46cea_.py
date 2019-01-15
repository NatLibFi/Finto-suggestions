"""Removed access_token table from database for security reason also

Revision ID: 224ae0a46cea
Revises: ee5b145411ae
Create Date: 2019-01-14 14:06:48.802483

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '224ae0a46cea'
down_revision = 'ee5b145411ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('access_token')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('access_token',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('provider', sa.VARCHAR(length=36), autoincrement=False, nullable=False),
    sa.Column('code', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('access_token', sa.VARCHAR(length=400), autoincrement=False, nullable=False),
    sa.Column('refresh_token', sa.VARCHAR(length=400), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='access_token_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='access_token_pkey')
    )
    # ### end Alembic commands ###
