from sqlalchemy import Column, Integer, PrimaryKeyConstraint, Text, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()
metadata = Base.metadata

class Vlans(Base):
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

    def __repr__(self):
        return f"Vlans(id={self.id!r}, vlan_id={self.vlan_id}, name={self.cost} ," \
               f"description={self.description}, created_at={self.created_at}, "\
               f"updated_at={self.updated_at}, "

class Devices(Base):
    __tablename__ = 'devices'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='devices_pkey'),
    )

    id = Column(Integer)
    hostname = Column(Text)
    ip_address = Column(Text, nullable=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __repr__(self):
        return f"Devices(id={self.id!r}, hostname={self.hostname}, "\
               f"ip_address={self.ip_address}, created_at={self.created_at}, "\
               f"updated_at={self.updated_at}, "
