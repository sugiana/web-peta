from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    )
from sqlalchemy.orm import (
    relationship,
    declarative_base,
    )
from sqlalchemy.dialects.postgresql import JSONB
from geoalchemy2 import Geometry


Base = declarative_base()


class Wilayah(Base):
    __tablename__ = 'wilayah'
    id = Column(Integer, primary_key=True)
    key = Column(String(16), unique=True, nullable=False)
    wilayah_id = Column(Integer, ForeignKey('wilayah.id'))
    tingkat_id = Column(Integer, nullable=False)
    nama_lengkap = Column(String(256), nullable=False)
    batas = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326))
    data = Column(JSONB)
    parent = relationship('Wilayah', remote_side=[id])
