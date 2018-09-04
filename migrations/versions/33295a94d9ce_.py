"""empty message

Revision ID: 33295a94d9ce
Revises: c1b178d802eb
Create Date: 2018-08-13 13:57:08.075558

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '33295a94d9ce'
down_revision = 'c1b178d802eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('telephone', sa.String(length=11), nullable=False),
    sa.Column('password', sa.String(length=64), nullable=False),
    sa.Column('about_me', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('telephone'),
    sa.UniqueConstraint('username')
    )
    op.drop_index('telephone', table_name='users')
    op.drop_index('username', table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('username', mysql.VARCHAR(length=64), nullable=False),
    sa.Column('telephone', mysql.VARCHAR(length=11), nullable=False),
    sa.Column('password', mysql.VARCHAR(length=64), nullable=False),
    sa.Column('about_me', mysql.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_index('username', 'users', ['username'], unique=True)
    op.create_index('telephone', 'users', ['telephone'], unique=True)
    op.drop_table('user')
    # ### end Alembic commands ###
