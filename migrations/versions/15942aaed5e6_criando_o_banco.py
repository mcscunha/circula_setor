"""Criando o banco

Revision ID: 15942aaed5e6
Revises: 
Create Date: 2019-12-01 16:18:18.575865

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15942aaed5e6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('setor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('setor', sa.String(length=100), nullable=True),
    sa.Column('ativo', sa.String(length=1), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_setor_setor'), 'setor', ['setor'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('about_me', sa.String(length=140), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('comunicado',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('idUsuario', sa.Integer(), nullable=True),
    sa.Column('idSetorOrigem', sa.Integer(), nullable=True),
    sa.Column('dtCadastro', sa.DateTime(), nullable=True),
    sa.Column('titulo', sa.String(length=100), nullable=True),
    sa.Column('comunicado', sa.Text(), nullable=True),
    sa.Column('apagado', sa.String(length=1), nullable=True),
    sa.ForeignKeyConstraint(['idSetorOrigem'], ['setor.id'], ),
    sa.ForeignKeyConstraint(['idUsuario'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comunicado_titulo'), 'comunicado', ['titulo'], unique=False)
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    op.create_table('comunicado_setor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('idComunicado', sa.Integer(), nullable=True),
    sa.Column('idSetor', sa.Integer(), nullable=True),
    sa.Column('hrLeitura', sa.Time(), nullable=True),
    sa.ForeignKeyConstraint(['idComunicado'], ['comunicado.id'], ),
    sa.ForeignKeyConstraint(['idSetor'], ['setor.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('log_comunicado',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('idComunicado', sa.Integer(), nullable=True),
    sa.Column('idUsuario', sa.Integer(), nullable=True),
    sa.Column('dtCadastro', sa.Date(), nullable=True),
    sa.Column('hrCadastro', sa.Time(), nullable=True),
    sa.ForeignKeyConstraint(['idComunicado'], ['comunicado.id'], ),
    sa.ForeignKeyConstraint(['idUsuario'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('log_comunicado')
    op.drop_table('comunicado_setor')
    op.drop_table('followers')
    op.drop_index(op.f('ix_comunicado_titulo'), table_name='comunicado')
    op.drop_table('comunicado')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_setor_setor'), table_name='setor')
    op.drop_table('setor')
    # ### end Alembic commands ###