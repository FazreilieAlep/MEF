from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .....core.database import Base
from ...associations import series_creators

class Creator(Base):
    __tablename__ = "creators"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    series = relationship("Series", secondary=series_creators, back_populates="creators")