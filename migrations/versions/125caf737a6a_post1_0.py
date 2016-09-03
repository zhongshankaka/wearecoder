"""post1.0

Revision ID: 125caf737a6a
Revises: 4a95cc52c7ff
Create Date: 2016-09-03 21:17:07.866275

"""

# revision identifiers, used by Alembic.
revision = '125caf737a6a'
down_revision = '4a95cc52c7ff'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_posts_timestamp', 'posts', ['timestamp'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_posts_timestamp', 'posts')
    op.drop_table('posts')
    ### end Alembic commands ###
