from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .....core.database import Base
from ...associations import movie_directors

class Director(Base):
    __tablename__ = "directors"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    movies = relationship("Movie", secondary=movie_directors, back_populates="directors")