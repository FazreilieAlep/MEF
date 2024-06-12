from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .....core.database import Base

class Alternative_Titles(Base):
    __tablename__ = "alternative_titles"

    id = Column(Integer, primary_key=True, index=True)
    synonym = Column(String)
    japanese = Column(String)
    anime_id = Column(Integer, ForeignKey("animes.id"))
    
    anime = relationship("Anime", back_populates="alternative_titles")