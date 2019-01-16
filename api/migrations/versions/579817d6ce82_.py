"""Assigning user to suggestion needed add user_id relation to suggestion table

Revision ID: 579817d6ce82
Revises: 5b7add77d694
Create Date: 2018-12-04 11:53:53.797717

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '579817d6ce82'
down_revision = '5b7add77d694'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('suggestions', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'suggestions', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'suggestions', type_='foreignkey')
    op.drop_column('suggestions', 'user_id')
    # ### end Alembic commands ###
