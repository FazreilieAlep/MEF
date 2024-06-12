from sqlalchemy import Column, Integer, String, Float, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from .....core.database import Base
from ...associations import movie_genres, movie_stars, movie_directors, movie_countries, movie_languages
from ...star.star import Star
from ..director.director import Director
from ...country.country import Country
from ...language.language import Language

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    imdb_id = Column(String, nullable=False)
    title = Column(String)
    description = Column(String)
    tagline = Column(String)
    year = Column(Integer)
    release_date = Column(Date)
    imdb_rating = Column(Float)
    vote_count_number = Column(Integer)
    popularity = Column(Float)
    youtube_trailer_key = Column(String)
    runtime = Column(Integer)
    rated_id = Column(Integer, ForeignKey('enums.id'))
    
    genres = relationship("Enums", secondary=movie_genres, back_populates="genre_movies")
    stars = relationship("Star", secondary=movie_stars, back_populates="movies")
    directors = relationship("Director", secondary=movie_directors, back_populates="movies")
    countries = relationship("Country", secondary=movie_countries, back_populates="movies")
    languages = relationship("Language", secondary=movie_languages, back_populates="movies")
    
    rated = relationship("Enums", foreign_keys=[rated_id], back_populates="rated_movies")
