"""empty message

Revision ID: 69234aa61a1f
Revises:
Create Date: 2018-05-29 09:38:14.140640

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69234aa61a1f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hook',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('repo_id', sa.Integer(), nullable=True),
    sa.Column('repo_name', sa.String(), nullable=True),
    sa.Column('repo_owner', sa.String(), nullable=True),
    sa.Column('subscribe_uuid', sa.String(), nullable=True),
    sa.Column('github_hook_secret', sa.String(), nullable=True),
    sa.Column('github_hook_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=200), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('github_nb_followers', sa.Integer(), nullable=True),
    sa.Column('github_nb_following', sa.Integer(), nullable=True),
    sa.Column('github_access_token', sa.String(length=200), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('pivot',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('consumer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pivot_id', sa.Integer(), nullable=True),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('url_path', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('ctype', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['pivot_id'], ['pivot.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('producer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pivot_id', sa.Integer(), nullable=True),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('url_path', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('ptype', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['pivot_id'], ['pivot.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('producer')
    op.drop_table('consumer')
    op.drop_table('pivot')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('hook')
    # ### end Alembic commands ###
