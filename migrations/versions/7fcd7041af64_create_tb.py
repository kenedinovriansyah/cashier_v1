"""create tb

Revision ID: 7fcd7041af64
Revises: 
Create Date: 2021-08-24 05:11:58.251195

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fcd7041af64'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tb_user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('public_id', sa.String(length=255), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=225), nullable=False),
    sa.Column('createAt', sa.DateTime(), nullable=True),
    sa.Column('updateAt', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('public_id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('tb_daily_price',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('public_id', sa.String(length=225), nullable=False),
    sa.Column('price_date', sa.DateTime(), nullable=False),
    sa.Column('createAt', sa.DateTime(), nullable=True),
    sa.Column('updateAt', sa.DateTime(), nullable=False),
    sa.Column('open_price', sa.Numeric(precision=11, scale=4), nullable=False),
    sa.Column('high_price', sa.Numeric(precision=11, scale=4), nullable=False),
    sa.Column('low_price', sa.Numeric(precision=11, scale=4), nullable=False),
    sa.Column('close_price', sa.Numeric(precision=11, scale=4), nullable=False),
    sa.Column('users_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['users_id'], ['tb_user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('public_id')
    )
    op.create_table('tb_vendor',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('createAt', sa.DateTime(), nullable=True),
    sa.Column('updateAt', sa.DateTime(), nullable=False),
    sa.Column('daily_price_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['daily_price_id'], ['tb_daily_price.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tb_vendor')
    op.drop_table('tb_daily_price')
    op.drop_table('tb_user')
    # ### end Alembic commands ###
