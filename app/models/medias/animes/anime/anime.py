from enum import unique
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .....core.database import Base
from ...associations import anime_producers, anime_licensors, anime_studios, anime_genres, anime_demographics
from ..alternative_titles.alternative_titles import Alternative_Titles
from ..information.information import Information

class Anime(Base):
    __tablename__ = "animes"

    id = Column(Integer, primary_key=True)
    myanimelist_id = Column(Integer, unique=True, nullable=True)
    title_ov = Column(String, unique=True, nullable=False)
    title_en = Column(String)
    synopsis = Column(String)
    picture_url = Column(String)
    type_id = Column(Integer, ForeignKey("enums.id"))
    premier_id = Column(Integer, ForeignKey("premiers.id"))

    alternative_titles = relationship("Alternative_Titles", back_populates="anime", uselist=False, cascade="all, delete-orphan")
    information = relationship("Information", back_populates="anime", uselist=False, cascade="all, delete-orphan")
    
    producers = relationship("Producer", secondary=anime_producers, back_populates="produced")
    licensors = relationship("Licensor", secondary=anime_licensors, back_populates="licensed")
    studios = relationship("Studio", secondary=anime_studios, back_populates="created")
    genres = relationship("Enums", secondary=anime_genres, back_populates="genre_animes")
    demographics = relationship("Enums", secondary=anime_demographics, back_populates="demographic_animes")
    
    type = relationship("Enums", foreign_keys=[type_id], back_populates="type_animes")
    premiered = relationship("Premier", foreign_keys=[premier_id], back_populates="anime")