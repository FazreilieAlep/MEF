from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from ...associations import series_genres, series_stars, series_countries, series_languages, series_creators, series_production_companies, series_networks
from ..creator.creator import Creator
from ...country.country import Country
from ...language.language import Language
from ..production.production import Production
from ..network.network import Network

class Series(Base):
    __tablename__ = "series"

    id = Column(Integer, primary_key=True)
    imdb_id = Column(String, nullable=False)
    title = Column(String, unique=True, nullable=False)
    description = Column(String)
    year_started = Column(Integer)
    release_date = Column(String)
    imdb_rating = Column(Float)
    vote_count = Column(Integer)
    popularity = Column(Float)
    youtube_trailer_key = Column(String)
    runtime = Column(Integer)
    rated_id = Column(Integer, ForeignKey('enums.id'))
    
    genres = relationship("Enums", secondary=series_genres, back_populates="genre_series")
    stars = relationship("Star", secondary=series_stars, back_populates="series")
    creators = relationship("Creator", secondary=series_creators, back_populates="series")
    countries = relationship("Country", secondary=series_countries, back_populates="series")
    languages = relationship("Language", secondary=series_languages, back_populates="series")
    production_companies = relationship("Production", secondary=series_production_companies, back_populates="series")
    networks = relationship("Network", secondary=series_networks, back_populates="series")
    
    rated = relationship("Enums", back_populates="rated_series", foreign_keys=[rated_id])