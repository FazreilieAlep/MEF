from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ....core.database import Base
from ..associations import movie_countries, series_countries

class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    movies = relationship("Movie", secondary=movie_countries, back_populates="countries")
    series = relationship("Series", secondary=series_countries, back_populates="countries")
