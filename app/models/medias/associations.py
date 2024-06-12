from sqlalchemy import Table, Column, Integer, ForeignKey
from app.core.database import Base

# Association tables for many-to-many relationships

# ANIMES ASSOCIATION
anime_producers = Table(
    'anime_producers', Base.metadata,
    Column('anime_id', Integer, ForeignKey('animes.id'), primary_key=True),
    Column('producer_id', Integer, ForeignKey('producers.id'), primary_key=True)
)

anime_licensors = Table(
    'anime_licensors', Base.metadata,
    Column('anime_id', Integer, ForeignKey('animes.id'), primary_key=True),
    Column('licensor_id', Integer, ForeignKey('licensors.id'), primary_key=True)
)

anime_studios = Table(
    'anime_studios', Base.metadata,
    Column('anime_id', Integer, ForeignKey('animes.id'), primary_key=True),
    Column('studio_id', Integer, ForeignKey('studios.id'), primary_key=True)
)

anime_genres = Table(
    'anime_genres', Base.metadata,
    Column('anime_id', Integer, ForeignKey('animes.id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('enums.id'), primary_key=True)
)

anime_demographics = Table(
    'anime_demographics', Base.metadata,
    Column('anime_id', Integer, ForeignKey('animes.id'), primary_key=True),
    Column('demographic_id', Integer, ForeignKey('enums.id'), primary_key=True)
)


# MOVIES ASSOCIATIONS
movie_genres = Table(
    'movie_genres', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('enums.id'), primary_key=True)
)

movie_stars = Table(
    'movie_stars', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True),
    Column('star_id', Integer, ForeignKey('stars.id'), primary_key=True)
)

movie_directors = Table(
    'movie_directors', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True),
    Column('director_id', Integer, ForeignKey('directors.id'), primary_key=True)
)

movie_countries = Table(
    'movie_countries', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True),
    Column('country_id', Integer, ForeignKey('countries.id'), primary_key=True)
)

movie_languages = Table(
    'movie_languages', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True),
    Column('language_id', Integer, ForeignKey('languages.id'), primary_key=True)
)

# SERIES ASSOCIATION
series_genres = Table(
    'series_genres', Base.metadata,
    Column('series_id', Integer, ForeignKey('series.id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('enums.id'), primary_key=True)
)

series_stars = Table(
    'series_stars', Base.metadata,
    Column('series_id', Integer, ForeignKey('series.id'), primary_key=True),
    Column('star_id', Integer, ForeignKey('stars.id'), primary_key=True)
)

series_creators = Table(
    'series_creators', Base.metadata,
    Column('series_id', Integer, ForeignKey('series.id'), primary_key=True),
    Column('creator_id', Integer, ForeignKey('creators.id'), primary_key=True)
)

series_countries = Table(
    'series_countries', Base.metadata,
    Column('series_id', Integer, ForeignKey('series.id'), primary_key=True),
    Column('country_id', Integer, ForeignKey('countries.id'), primary_key=True)
)

series_languages = Table(
    'series_languages', Base.metadata,
    Column('series_id', Integer, ForeignKey('series.id'), primary_key=True),
    Column('language_id', Integer, ForeignKey('languages.id'), primary_key=True)
)

series_production_companies = Table(
    'series_production_companies', Base.metadata,
    Column('series_id', Integer, ForeignKey('series.id'), primary_key=True),
    Column('production_id', Integer, ForeignKey('productions.id'), primary_key=True)
)

series_networks = Table(
    'series_networks', Base.metadata,
    Column('series_id', Integer, ForeignKey('series.id'), primary_key=True),
    Column('network_id', Integer, ForeignKey('networks.id'), primary_key=True)
)