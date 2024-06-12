from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ....core.database import Base
from ..associations import movie_stars, series_stars
from ..series.series.series import Series

class Star(Base):
    __tablename__ = "stars"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    movies = relationship("Movie", secondary=movie_stars, back_populates="stars")
    series = relationship("Series", secondary=series_stars, back_populates="stars")