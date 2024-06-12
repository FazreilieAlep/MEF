from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .....core.database import Base
from ...associations import series_production_companies

class Production(Base):
    __tablename__ = "productions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    series = relationship("Series", secondary=series_production_companies, back_populates="production_companies")