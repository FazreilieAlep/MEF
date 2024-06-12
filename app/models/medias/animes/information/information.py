from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .....core.database import Base

class Information(Base):
    __tablename__ = "informations"

    id = Column(Integer, primary_key=True, index=True)
    episode = Column(Integer)
    aired = Column(String)
    broadcast = Column(String)
    anime_id = Column(Integer, ForeignKey("animes.id"))
    status_id = Column(Integer, ForeignKey("enums.id"))
    
    anime = relationship("Anime", back_populates="information")
    status = relationship("Enums", foreign_keys=[status_id])
    
    