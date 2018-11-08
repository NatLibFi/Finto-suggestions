"""Init db default values

Revision ID: e008d81a779e
Revises: 
Create Date: 2018-08-15 14:15:20.856976

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e008d81a779e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('meetings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('meeting_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_meetings_created'), 'meetings', ['created'], unique=False)
    op.create_index(op.f('ix_meetings_meeting_date'), 'meetings', ['meeting_date'], unique=False)
    op.create_index(op.f('ix_meetings_modified'), 'meetings', ['modified'], unique=False)
    op.create_table('tags',
    sa.Column('label', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('label')
    )
    op.create_index(op.f('ix_tags_label'), 'tags', ['label'], unique=False)
    op.create_table('tokens_blacklist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jti', sa.String(length=36), nullable=False),
    sa.Column('token_type', sa.String(length=10), nullable=False),
    sa.Column('revoked', sa.Boolean(), nullable=False),
    sa.Column('expires', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('role', sa.Enum('NORMAL', 'ADMIN', name='userroles'), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_created'), 'users', ['created'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_name'), 'users', ['name'], unique=False)
    op.create_table('suggestions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('suggestion_type', sa.Enum('NEW', 'MODIFY', name='suggestiontypes'), nullable=True),
    sa.Column('status', sa.Enum('DEFAULT', 'REJECTED', 'ACCEPTED', name='suggestionstatustypes'), nullable=True),
    sa.Column('uri', sa.String(length=256), nullable=True),
    sa.Column('organization', sa.String(length=256), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('reason', sa.Text(), nullable=True),
    sa.Column('preferred_label', sa.JSON(), nullable=True),
    sa.Column('alternative_label', sa.JSON(), nullable=True),
    sa.Column('broader', sa.JSON(), nullable=True),
    sa.Column('narrower', sa.JSON(), nullable=True),
    sa.Column('related', sa.JSON(), nullable=True),
    sa.Column('group', sa.JSON(), nullable=True),
    sa.Column('meeting_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['meeting_id'], ['meetings.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_suggestions_created'), 'suggestions', ['created'], unique=False)
    op.create_index(op.f('ix_suggestions_modified'), 'suggestions', ['modified'], unique=False)
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('event_type', sa.Enum('ACTION', 'COMMENT', name='eventtypes'), nullable=False),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('suggestion_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['suggestion_id'], ['suggestions.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_events_created'), 'events', ['created'], unique=False)
    op.create_index(op.f('ix_events_modified'), 'events', ['modified'], unique=False)
    op.create_table('suggestion_tags_association',
    sa.Column('tag_label', sa.String(), nullable=False),
    sa.Column('suggestion_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['suggestion_id'], ['suggestions.id'], ),
    sa.ForeignKeyConstraint(['tag_label'], ['tags.label'], ),
    sa.PrimaryKeyConstraint('tag_label', 'suggestion_id')
    )
    op.create_table('reactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=32), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.Column('suggestion_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.ForeignKeyConstraint(['suggestion_id'], ['suggestions.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reactions')
    op.drop_table('suggestion_tags_association')
    op.drop_index(op.f('ix_events_modified'), table_name='events')
    op.drop_index(op.f('ix_events_created'), table_name='events')
    op.drop_table('events')
    op.drop_index(op.f('ix_suggestions_modified'), table_name='suggestions')
    op.drop_index(op.f('ix_suggestions_created'), table_name='suggestions')
    op.drop_table('suggestions')
    op.drop_index(op.f('ix_users_name'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_created'), table_name='users')
    op.drop_table('users')
    op.drop_table('tokens_blacklist')
    op.drop_index(op.f('ix_tags_label'), table_name='tags')
    op.drop_table('tags')
    op.drop_index(op.f('ix_meetings_modified'), table_name='meetings')
    op.drop_index(op.f('ix_meetings_meeting_date'), table_name='meetings')
    op.drop_index(op.f('ix_meetings_created'), table_name='meetings')
    op.drop_table('meetings')
    # ### end Alembic commands ###
