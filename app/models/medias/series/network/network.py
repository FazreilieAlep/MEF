from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .....core.database import Base
from ...associations import series_networks

class Network(Base):
    __tablename__ = "networks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    series = relationship("Series", secondary=series_networks, back_populates="networks")