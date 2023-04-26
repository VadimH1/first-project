"""empty message

Revision ID: 504bd477e346
Revises: cb315b00c346
Create Date: 2023-04-26 18:22:47.904347

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '504bd477e346'
down_revision = 'cb315b00c346'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('upload', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key("fk_upload_author_id", 'user', ['author_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('upload', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('author_id')

    # ### end Alembic commands ###
