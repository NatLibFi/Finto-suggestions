"""Update alternative_labels's type to JSON instead of array of JSON's

Revision ID: 1ce8294d773d
Revises: 61fa3cf3732a
Create Date: 2019-02-11 17:01:17.913843

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1ce8294d773d'
down_revision = '61fa3cf3732a'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('suggestions', 'alternative_labels',
                new_column_name='outdated_alternative_labels')

    op.drop_column('suggestions', 'outdated_alternative_labels')

    op.add_column('suggestions',
                sa.Column('alternative_labels',
                sa.JSON(),
                nullable=True))


def downgrade():
    op.alter_column('suggestions', 'alternative_labels',
                new_column_name='outdated_alternative_labels')

    op.drop_column('suggestions', 'outdated_alternative_labels')

    op.add_column('suggestions',
                sa.Column('alternative_labels',
                postgresql.ARRAY(postgresql.JSON(astext_type=sa.Text())),
                nullable=True))