"""initial db setup

Revision ID: f8e0642cb95b
Revises: 
Create Date: 2023-08-07 16:55:43.793955

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TIMESTAMP

# revision identifiers, used by Alembic.
revision: str = 'f8e0642cb95b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('vlans',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('vlan_id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.Text(), nullable=False),
                    sa.Column('description', sa.Text(), nullable=False),
                    sa.PrimaryKeyConstraint('id', name='vlans_pkey'),
                    sa.Column('created_at', TIMESTAMP, server_default=sa.func.now()),
                    sa.Column('updated_at', TIMESTAMP, onupdate=sa.func.now()),
                    sa.Column('device_id', sa.Integer(), nullable=True)
    )

    op.create_table('devices',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('hostname', sa.Text(), nullable=False),
                    sa.Column('ip_address', sa.Text(), nullable=True),
                    sa.PrimaryKeyConstraint('id', name='devices_pkey'),
                    sa.Column('created_at', TIMESTAMP, server_default=sa.func.now()),
                    sa.Column('updated_at', TIMESTAMP, onupdate=sa.func.now()),
                    sa.Column('vlan_id', sa.Integer(), nullable=True)
    )

    op.create_table('devices_and_vlans',
                    sa.Column('device_id', sa.Integer(), nullable=True),
                    sa.Column('vlan_id', sa.Integer(), nullable=True),
    )

    op.create_foreign_key('foreign_key_devices_id_vlans_id','devices', 'vlans', ['vlan_id'], ['id'], onupdate="CASCADE", ondelete="RESTRICT")

    op.create_foreign_key('foreign_key_vlans_id_devices_id', 'vlans', 'devices', ['device_id'], ['id'],
                          onupdate="CASCADE", ondelete="RESTRICT")

    op.create_unique_constraint('uq_hostname', 'devices', ['hostname'])

    op.create_unique_constraint('uq_vlan_id', 'vlans', ['vlan_id'])

def downgrade() -> None:
    op.drop_constraint('foreign_key_vlans_id_devices_id', 'vlans')

    op.drop_constraint('foreign_key_devices_id_vlans_id', 'devices')

    op.drop_constraint('uq_hostname', 'devices', 'unique')

    op.drop_constraint('uq_vlan_id', 'vlans', 'unique')

    op.drop_table('vlans')

    op.drop_table('devices')

    op.drop_table('devices_and_vlans')