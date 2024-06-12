from http.client import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import schema
from .movie import Movie
from ...crud import get_or_create_direct, get_or_create
from ...enums.enums import Enums
from ...host import Host
from ...enums_type import EnumsType

from ...star.star import Star
from ..director.director import Director
from ...country.country import Country
from ...language.language import Language

from ...enums.schema import EnumsCreateOrUpdate
from ...star.schema import StarCreateOrUpdate
from ..director.schema import DirectorCreateOrUpdate
from ...country.schema import CountryCreateOrUpdate
from ...language.schema import LanguageCreateOrUpdate

from typing import Type, Dict, Any, Optional, List, TypeVar
from sqlalchemy.ext.declarative import DeclarativeMeta
import logging

logging.basicConfig(level=logging.INFO)

T = TypeVar('T', bound=DeclarativeMeta)
BaseModel = TypeVar('BaseModel')

def get_movie_by_title(db: Session, title: str):
    return db.query(Movie).filter(Movie.title == title.lower()).first()

def get_movie_list(
    db: Session, 
    limit: int, 
    skip: int, 
    titles: Optional[List[str]], 
    genres: Optional[List[str]], 
    stars: Optional[List[str]], 
    directors: Optional[List[str]], 
    countries: Optional[List[str]], 
    languages: Optional[List[str]]
):
    query = db.query(Movie)

    if titles:
        titles = [title.lower() for title in titles]
        title_conditions = [Movie.title.ilike(f"%{title}%") for title in titles]
        query = query.filter(or_(*title_conditions))

    if genres:
        genres = [genre.lower() for genre in genres]
        genre_conditions = [Enums.value.ilike(f"%{genre}%") for genre in genres]
        query = query.filter(Movie.genres.any(or_(*genre_conditions)))

    if stars:
        stars = [star.lower() for star in stars]
        star_conditions = [Star.name.ilike(f"%{star}%") for star in stars]
        query = query.filter(Movie.stars.any(or_(*star_conditions)))

    if directors:
        directors = [director.lower() for director in directors]
        director_conditions = [Director.name.ilike(f"%{director}%") for director in directors]
        query = query.filter(Movie.directors.any(or_(*director_conditions)))

    if countries:
        countries = [country.lower() for country in countries]
        country_conditions = [Country.name.ilike(f"%{country}%") for country in countries]
        query = query.filter(Movie.countries.any(or_(*country_conditions)))

    if languages:
        languages = [language.lower() for language in languages]
        language_conditions = [Language.name.ilike(f"%{language}%") for language in languages]
        query = query.filter(Movie.languages.any(or_(*language_conditions)))

    return query.offset(skip).limit(limit).all()


def get_movie_by_item_id(db: Session, item: str, item_id: int, limit: int, skip: int) -> List[Movie]:
    query = db.query(Movie)
    
    if item == 'genre':
        query = query.join(Enums, Movie.genres).filter(
            Enums.id == item_id,
            Enums.site == Host._1MDB,
            Enums.type == EnumsType.GENRE
        )
    elif item == 'star':
        query = query.join(Star, Movie.stars).filter(Star.id == item_id)
    elif item == 'director':
        query = query.join(Director, Movie.directors).filter(Director.id == item_id)
    elif item == 'country':
        query = query.join(Country, Movie.countries).filter(Country.id == item_id)
    elif item == 'language':
        query = query.join(Language, Movie.languages).filter(Language.id == item_id)
    elif item == 'rated':
        query = query.filter(Movie.rated_id == item_id)
    
    return query.offset(skip).limit(limit).all()

def get_item_list(db: Session, item: str, limit: int, skip: int) -> List:
    if item == 'genre':
        return db.query(Enums).filter(
            Enums.site == Host._1MDB, 
            Enums.type == EnumsType.GENRE).offset(skip).limit(limit).all()
    elif item == 'star':
        return db.query(Star).offset(skip).limit(limit).all()
    elif item == 'director':
        return db.query(Director).offset(skip).limit(limit).all()
    elif item == 'country':
        return db.query(Country).offset(skip).limit(limit).all()
    elif item == 'language':
        return db.query(Language).offset(skip).limit(limit).all()
    elif item == 'rated':
        return db.query(Enums).filter(
            Enums.site == Host._1MDB, 
            Enums.type == EnumsType.RATED).offset(skip).limit(limit).all()
    return []

def create_movie(db: Session, movie=schema.MovieCreate):
    
    # Create or get related objects
    rated = get_or_create_direct(db, Enums, value = movie.rated.lower(), site = Host._1MDB, type = EnumsType.RATED) if movie.rated else None
    genres = [get_or_create_direct(db, Enums, value = genre.lower(), site =  Host._1MDB, type = EnumsType.GENRE) for genre in movie.genres] if movie.genres else []
    stars = [get_or_create_direct(db, Star, name = star.lower()) for star in list(set([star.lower() for star in movie.stars]))] if movie.stars else []
    directors = [get_or_create_direct(db, Director, name = director.lower()) for director in list(set([director.lower() for director in movie.directors]))] if movie.directors else []
    countries = [get_or_create_direct(db, Country, name = country.lower()) for country in list(set([country.lower() for country in movie.countries]))] if movie.countries else []
    languages = [get_or_create_direct(db, Language, name = language.lower()) for language in list(set([language.lower() for language in movie.language]))] if movie.language else []
  
    # Create main movie object
    db_movie = get_movie_by_title(db, movie.title)
    if db_movie is None:
        db_movie = Movie(
            id=movie.id,
            imdb_id=movie.imdb_id, 
            title=movie.title.lower(),
            description=movie.description,
            tagline=movie.tagline,
            year=movie.year,
            release_date=movie.release_date,
            imdb_rating=movie.imdb_rating,
            vote_count_number=movie.vote_count,
            popularity=movie.popularity,
            youtube_trailer_key=movie.youtube_trailer_key,
            runtime=movie.runtime,
            rated_id=rated.id if rated else None,
        )
  
        # Add to session
        db.add(db_movie)
        db.commit()
        db.refresh(db_movie)
     # Create and associate related objects
    db_movie.genres = genres
    db_movie.stars = stars
    db_movie.directors = directors
    db_movie.countries = countries
    db_movie.languages = languages
    db.commit()
    db.refresh(db_movie)
    
    return db_movie


def delete_movie(db: Session, movie_id: str):
    # First, try to fetch the movie by ID
    movie = db.query(Movie).filter((Movie.id == movie_id) | (Movie.imdb_id == movie_id)).first()
    
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    temp_name = movie.title
    db.delete(movie)
    db.commit()
    return {"detail": f"'{temp_name}' with ID '{movie_id}' deleted successfully"}


def update_relationship(db: Session, db_movie, field_name: str, related_model, related_data_list: List[str], related_schema: Type[T], **kwargs):
    enums_field = ["genres"]
    logging.info(f"Updating relationship for field: {field_name}")

    current_items = getattr(db_movie, field_name)
    current_items_dict = {item.id: item for item in current_items}

    new_items = []
    for item_data in related_data_list:
        item_value = item_data.lower() 
        if item_value:
            if field_name not in enums_field:
                item = get_or_create(db, related_model, {"name" : item_value})
            else:
                item = get_or_create(db, related_model, {"value" : item_value, **kwargs})
        else:
            logging.warning("Item data does not contain id or name")
            continue

        new_items.append(item)

    # Remove items not in the new list
    for item in list(current_items):  # Use list to avoid modification during iteration
        if item.id not in [new_item.id for new_item in new_items]:
            current_items.remove(item)

    # Add new items
    for item in new_items:
        if item.id not in [current_item.id for current_item in current_items]:
            current_items.append(item)

    # Commit and refresh once after all changes
    db.commit()
    db.refresh(db_movie)
    logging.info(f"Updated {field_name} with new items")
    
    
def update_movie(db: Session, movie: schema.MovieUpdate):
    db_movie = db.query(Movie).filter(Movie.id == movie.id).first()
    if not db_movie:
        return None
    
    update_data = movie.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if key not in {"rated", "genres", "stars", "directors", "countries", "languages"} and value is not None:
            setattr(db_movie, key, value)

    relationship_fields = {
        "genres": (Enums, EnumsCreateOrUpdate),
        "stars": (Star, StarCreateOrUpdate),
        "directors": (Director, DirectorCreateOrUpdate),
        "countries": (Country, CountryCreateOrUpdate),
        "languages": (Language, LanguageCreateOrUpdate)
    }
    
    for field, (model, create_or_update) in relationship_fields.items():
        if field in update_data:
            kwargs = {}
            if field in {"genres"}:
                kwargs["site"] = Host._1MDB
                kwargs["type"] = EnumsType.GENRE
            update_relationship(db, db_movie, field, model, update_data[field], create_or_update, **kwargs)

    if "rated" in update_data:
        rated_instance = get_or_create(db, Enums, 
                              {
                                  "value" : update_data["rated"].lower(), 
                                  "site":Host._1MDB, "type":EnumsType.RATED
                              }, 
                              url=None)
        if rated_instance:
            db_movie.rated = rated_instance
            db_movie.rated_id = rated_instance.id
    
    db.commit()
    db.refresh(db_movie)
    return db_movie