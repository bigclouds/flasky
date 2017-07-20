"""empty message

Revision ID: ff358ff469aa
Revises: 2c1113a29b91
Create Date: 2017-07-03 18:00:27.242400

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff358ff469aa'
down_revision = '2c1113a29b91'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('msgboxs', sa.Column('deleted', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('msgboxs', 'deleted')
    # ### end Alembic commands ###