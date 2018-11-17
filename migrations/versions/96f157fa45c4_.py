"""empty message

Revision ID: 96f157fa45c4
Revises: bb5bc7cf5bb1
Create Date: 2018-11-17 17:12:55.090872

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '96f157fa45c4'
down_revision = 'bb5bc7cf5bb1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('create_time', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_comments_create_time'), 'comments', ['create_time'], unique=False)
    op.drop_index('ix_comments_timestamp', table_name='comments')
    op.drop_column('comments', 'timestamp')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('timestamp', mysql.DATETIME(), nullable=True))
    op.create_index('ix_comments_timestamp', 'comments', ['timestamp'], unique=False)
    op.drop_index(op.f('ix_comments_create_time'), table_name='comments')
    op.drop_column('comments', 'create_time')
    # ### end Alembic commands ###