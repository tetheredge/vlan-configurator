"""initial db setup

Revision ID: f8e0642cb95b
Revises: 
Create Date: 2023-08-07 16:55:43.793955

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'f8e0642cb95b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('vlans',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('vlan_id', sa.Integer(), nullable=True),
                    sa.Column('name', sa.Text(), nullable=True),
                    sa.Column('description', sa.Text(), nullable=True),
                    sa.PrimaryKeyConstraint('id', name='vlans_pkey'),
                    sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
                    sa.Column('updated_at', sa.DateTime, onupdate=sa.func.now())
    )

    op.create_table('devices',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('hostname', sa.Text(), nullable=False),
                    sa.Column('ip_address', sa.Text(), nullable=True),
                    sa.PrimaryKeyConstraint('id', name='devices_pkey'),
                    sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
                    sa.Column('updated_at', sa.DateTime, onupdate=sa.func.now())
    )

    op.create_foreign_key('foreign_key_devices_id_vlans_id','devices', 'vlans', ['id'], ['id'], onupdate="CASCADE", ondelete="RESTRICT")

    op.create_foreign_key('foreign_key_vlans_id_devices_id', 'vlans', 'devices', ['id'], ['id'],
                          onupdate="CASCADE", ondelete="RESTRICT")

def downgrade() -> None:
    op.drop_constraint('foreign_key_vlans_id_devices_id', 'vlans')

    op.drop_constraint('foreign_key_devices_id_vlans_id', 'devices')

    op.drop_table('vlans')

    op.drop_table('devices')