from __future__ import annotations

from typing import List

from sqlalchemy import Column, Integer, PrimaryKeyConstraint, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, Mapped

import db

Base = declarative_base()
metadata = Base.metadata

devices_and_vlans = Table(
    'devices_and_vlans',
    Base.metadata,
    Column(
        'device_id',
        Integer,
        ForeignKey('devices.id', primary_key=True)
    ),
    Column(
        'vlan_id',
        Integer,
        ForeignKey('vlans.id', primary_key=True)
    )
)
class Vlan(Base):
    """Individual vlans belonging to a device."""

    __tablename__ = 'vlans'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='vlans_pkey'),
    )

    id = Column(Integer)
    vlan_id = Column(Integer)
    name = Column(Text)
    description = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    # Relationships
    devices: Mapped[List[Device]] = relationship("Device", secondary=devices_and_vlans, back_populates='vlans')

    def __repr__(self):
        return f"Vlan(id={self.id!r}, vlan_id={self.vlan_id}, name={self.name} ," \
               f"description={self.description}, created_at={self.created_at}, "\
               f"updated_at={self.updated_at})"

    def get_vlans(self):
        results = db.session.query(Vlan).all()

        return results

    def get_vlans_count(self):
        results = db.session.query(Vlan).count()

        return results

    def get_vlans_on_devices(self, vlan_id):
        result = db.session \
            .query(Vlan) \
            .filter(Vlan.vlan_id == vlan_id) \
            .first()
        all_devices = result.devices

        return all_devices

class Device(Base):
    __tablename__ = 'devices'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='devices_pkey'),
    )

    id = Column(Integer)
    hostname = Column(Text)
    ip_address = Column(Text, nullable=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    # Relationships
    vlans: Mapped[List[Vlan]] = relationship('Vlan', secondary=devices_and_vlans, back_populates='devices')

    def __repr__(self):
        return f"Device(id={self.id!r}, hostname={self.hostname}, "\
               f"ip_address={self.ip_address}, created_at={self.created_at}, "\
               f"updated_at={self.updated_at})"

    def get_devices(self):
        results = db.session.query(Device).all()

        return results

    def get_devices_count(self):
        results = db.session.query(Device).count()

        return results

    def get_device_vlans(self, hostname):
        result = db.session \
            .query(Device)\
            .filter(Device.hostname == hostname) \
            .first()
        all_vlans = result.vlans

        return all_vlans
