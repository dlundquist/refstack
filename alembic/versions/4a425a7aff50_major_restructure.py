"""major restructure

Revision ID: 4a425a7aff50
Revises: None
Create Date: 2014-03-07 11:20:58.899889

"""

# revision identifiers, used by Alembic.
revision = '4a425a7aff50'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'vendor',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('vendor_name', sa.String(length=80), nullable=True),
        sa.Column('contact_email', sa.String(length=120), nullable=True),
        sa.Column('contact_name', sa.String(length=120), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('contact_email'),
        sa.UniqueConstraint('vendor_name')
    )
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('vendor_id', sa.Integer(), nullable=True),
        sa.Column('name', sa.String(length=60), nullable=True),
        sa.Column('email', sa.String(length=200), nullable=True),
        sa.Column('email_verified', sa.Boolean(), nullable=True),
        sa.Column('openid', sa.String(length=200), nullable=True),
        sa.Column('authorized', sa.Boolean(), nullable=True),
        sa.Column('su', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['vendor_id'], ['vendor.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('openid')
    )
    op.create_table(
        'apikey',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=60), nullable=True),
        sa.Column('key', sa.String(length=200), nullable=True),
        sa.Column('openid', sa.String(length=200), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'cloud',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('label', sa.String(length=60), nullable=True),
        sa.Column('endpoint', sa.String(length=512), nullable=True),
        sa.Column('endpoint_v3', sa.String(length=512), nullable=True),
        sa.Column('admin_endpoint', sa.String(length=512), nullable=True),
        sa.Column('test_user', sa.String(length=80), nullable=True),
        sa.Column('admin_user', sa.String(length=80), nullable=True),
        sa.Column('version', sa.String(length=80), nullable=True),
        sa.Column('tempest_sha', sa.String(length=128), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'test',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('cloud_id', sa.Integer(), nullable=True),
        sa.Column('finished', sa.Boolean(), nullable=True),
        sa.Column('subunit', sa.String(length=4096), nullable=True),
        sa.Column('parsed', sa.String(length=4096), nullable=True),
        sa.ForeignKeyConstraint(['cloud_id'], ['cloud.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'test_status',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('test_id', sa.Integer(), nullable=True),
        sa.Column('message', sa.String(length=1024), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['test_id'], ['test.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('test_status')
    op.drop_table('test')
    op.drop_table('cloud')
    op.drop_table('apikey')
    op.drop_table('user')
    op.drop_table('vendor')
    ### end Alembic commands ###
