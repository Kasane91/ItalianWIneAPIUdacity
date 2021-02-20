"""empty message

Revision ID: 237452957750
Revises: 
Create Date: 2021-02-20 11:54:30.188292

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '237452957750'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('districts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('province', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('wines',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('producer', sa.String(length=100), nullable=False),
    sa.Column('vintage', sa.Integer(), nullable=False),
    sa.Column('grape', sa.Integer(), nullable=False),
    sa.Column('vinyard', sa.String(length=50), nullable=True),
    sa.Column('district_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['district_id'], ['districts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('wines')
    op.drop_table('districts')
    # ### end Alembic commands ###
