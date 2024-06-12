from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ....core.database import Base
from ..associations import movie_languages, series_languages

class Language(Base):
    __tablename__ = "languages"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    movies = relationship("Movie", secondary=movie_languages, back_populates="languages")
    series = relationship("Series", secondary=series_languages, back_populates="languages")
