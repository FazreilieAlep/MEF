from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from ....core.database import Base
from ..associations import anime_genres, anime_demographics, movie_genres, series_genres
from ...medias.host import Host
from ...medias.enums_type import EnumsType
from ..movies.movie.movie import Movie

class Enums(Base):
    __tablename__ = "enums"

    id = Column(Integer, primary_key=True, index=True)
    site = Column(Enum(Host), nullable=False)
    type = Column(Enum(EnumsType), nullable=False)  # genre or demographic, status, type
    value = Column(String, index=True, nullable=False)
    url = Column(String, nullable=True)

    genre_animes = relationship("Anime", secondary=anime_genres, back_populates="genres")
    demographic_animes = relationship("Anime", secondary=anime_demographics, back_populates="demographics")
    type_animes = relationship("Anime", back_populates="type")
    
    genre_movies = relationship("Movie", secondary=movie_genres, back_populates="genres")
    rated_movies = relationship("Movie", back_populates="rated")
    
    genre_series = relationship("Series", secondary=series_genres, back_populates="genres")
    rated_series = relationship("Series", back_populates="rated")