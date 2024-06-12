from http.client import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import schema
from .series import Series
from ...crud import get_or_create_direct, get_or_create
from ...enums.enums import Enums
from ...host import Host
from ...enums_type import EnumsType

from ...star.star import Star
from ..creator.creator import Creator
from ...country.country import Country
from ...language.language import Language
from ..production.production import Production
from ..network.network import Network

from ...enums.schema import EnumsCreateOrUpdate
from ...star.schema import StarCreateOrUpdate
from ..creator.schema import CreatorCreateOrUpdate
from ...country.schema import CountryCreateOrUpdate
from ...language.schema import LanguageCreateOrUpdate
from ..production.schema import ProductionCreateOrUpdate
from ..network.schema import NetworkCreateOrUpdate

from typing import Type, Dict, Any, Optional, List, TypeVar
from sqlalchemy.ext.declarative import DeclarativeMeta
import logging

logging.basicConfig(level=logging.INFO)

T = TypeVar('T', bound=DeclarativeMeta)
BaseModel = TypeVar('BaseModel')

def get_series_by_title(db: Session, title: str):
    return db.query(Series).filter(Series.title == title.lower()).first()

def get_series_list(
    db: Session, 
    limit: int, 
    skip: int, 
    titles: Optional[List[str]], 
    genres: Optional[List[str]], 
    stars: Optional[List[str]], 
    creators: Optional[List[str]], 
    countries: Optional[List[str]], 
    languages: Optional[List[str]],
    productions: Optional[List[str]], 
    networks: Optional[List[str]]
):
    query = db.query(Series)

    if titles:
        titles = [title.lower() for title in titles]
        title_conditions = [Series.title.ilike(f"%{title}%") for title in titles]
        query = query.filter(or_(*title_conditions))

    if genres:
        genres = [genre.lower() for genre in genres]
        genre_conditions = [Enums.value.ilike(f"%{genre}%") for genre in genres]
        query = query.filter(Series.genres.any(or_(*genre_conditions)))

    if stars:
        stars = [star.lower() for star in stars]
        star_conditions = [Star.name.ilike(f"%{star}%") for star in stars]
        query = query.filter(Series.stars.any(or_(*star_conditions)))

    if creators:
        creators = [creator.lower() for creator in creators]
        creator_conditions = [Creator.name.ilike(f"%{creator}%") for creator in creators]
        query = query.filter(Series.creators.any(or_(*creator_conditions)))

    if countries:
        countries = [country.lower() for country in countries]
        country_conditions = [Country.name.ilike(f"%{country}%") for country in countries]
        query = query.filter(Series.countries.any(or_(*country_conditions)))

    if languages:
        languages = [language.lower() for language in languages]
        language_conditions = [Language.name.ilike(f"%{language}%") for language in languages]
        query = query.filter(Series.languages.any(or_(*language_conditions)))
        
    if productions:
        productions = [production.lower() for production in productions]
        production_conditions = [Production.name.ilike(f"%{production}%") for production in productions]
        query = query.filter(Series.productions.any(or_(*production_conditions)))

    if networks:
        networks = [network.lower() for network in networks]
        network_conditions = [Network.name.ilike(f"%{network}%") for network in networks]
        query = query.filter(Series.networks.any(or_(*network_conditions)))

    return query.offset(skip).limit(limit).all()

def get_series_by_item_id(db: Session, item: str, item_id: int, limit: int, skip: int) -> List[Series]:
    query = db.query(Series)
    
    if item == 'genre':
        query = query.join(Enums, Series.genres).filter(
            Enums.id == item_id,
            Enums.site == Host._1MDB,
            Enums.type == EnumsType.GENRE
        )
    elif item == 'star':
        query = query.join(Star, Series.stars).filter(Star.id == item_id)
    elif item == 'creator':
        query = query.join(Creator, Series.creators).filter(Creator.id == item_id)
    elif item == 'country':
        query = query.join(Country, Series.countries).filter(Country.id == item_id)
    elif item == 'language':
        query = query.join(Language, Series.languages).filter(Language.id == item_id)
    elif item == 'production':
        query = query.join(Production, Series.production_companies).filter(Production.id == item_id)
    elif item == 'network':
        query = query.join(Network, Series.networks).filter(Network.id == item_id)
    elif item == 'rated':
        query = query.filter(Series.rated_id == item_id)
    
    return query.offset(skip).limit(limit).all()

def get_item_list(db: Session, item: str, limit: int, skip: int) -> List:
    if item == 'genre':
        return db.query(Enums).filter(
            Enums.site == Host._1MDB, 
            Enums.type == EnumsType.GENRE).offset(skip).limit(limit).all()
    elif item == 'star':
        return db.query(Star).offset(skip).limit(limit).all()
    elif item == 'creator':
        return db.query(Creator).offset(skip).limit(limit).all()
    elif item == 'country':
        return db.query(Country).offset(skip).limit(limit).all()
    elif item == 'language':
        return db.query(Language).offset(skip).limit(limit).all()
    elif item == 'production':
        return db.query(Production).offset(skip).limit(limit).all()
    elif item == 'network':
        return db.query(Network).offset(skip).limit(limit).all()
    elif item == 'rated':
        return db.query(Enums).filter(
            Enums.site == Host._1MDB, 
            Enums.type == EnumsType.RATED).offset(skip).limit(limit).all()
    return []

def create_series(db: Session, series=schema.SeriesCreate):
    
    # Create or get related objects
    rated = get_or_create_direct(db, Enums, value = series.rated.lower(), site = Host._1MDB, type = EnumsType.RATED) if series.rated else None
    genres = [get_or_create_direct(db, Enums, value = genre.lower(), site =  Host._1MDB, type = EnumsType.GENRE) for genre in series.genres] if series.genres else []
    stars = [get_or_create_direct(db, Star, name = star.lower()) for star in list(set([star.lower() for star in series.stars]))] if series.stars else []
    creators = [get_or_create_direct(db, Creator, name = creator.lower()) for creator in list(set([creator.lower() for creator in series.creators]))] if series.creators else []
    countries = [get_or_create_direct(db, Country, name = country.lower()) for country in list(set([country.lower() for country in series.countries]))] if series.countries else []
    languages = [get_or_create_direct(db, Language, name = language.lower()) for language in list(set([language.lower() for language in series.language]))] if series.language else []
    production_companies = [get_or_create_direct(db, Production, name = production.lower()) for production in list(set([production.lower() for production in series.production_companies]))] if series.production_companies else []
    networks = [get_or_create_direct(db, Network, name = network.lower()) for network in list(set([network.lower() for network in series.networks]))] if series.networks else []
    
    # Create main Anime object
    db_series = get_series_by_title(db, series.title)
    if db_series is None:
        db_series = Series(
            id=series.id,
            imdb_id=series.imdb_id, 
            title=series.title.lower(),
            description=series.description,
            year_started=series.year_started,
            release_date=series.release_date,
            imdb_rating=series.imdb_rating,
            vote_count=series.vote_count,
            popularity=series.popularity,
            youtube_trailer_key=series.youtube_trailer_key,
            runtime=series.runtime,
            rated_id=rated.id if rated else None,
        )
        
        # Add to session
        db.add(db_series)
        db.commit()
        db.refresh(db_series)
     # Create and associate related objects
    db_series.genres = genres
    db_series.stars = stars
    db_series.creators = creators
    db_series.countries = countries
    db_series.languages = languages
    db_series.production_companies = production_companies
    db_series.networks = networks
    
    db.commit()
    db.refresh(db_series)
    
    return db_series


def delete_series(db: Session, series_id: str):
    # First, try to fetch the series by ID
    series = db.query(Series).filter((Series.id == series_id) | (Series.imdb_id == series_id)).first()
    
    if not series:
        raise HTTPException(status_code=404, detail="series not found")

    temp_name = series.title
    db.delete(series)
    db.commit()
    return {"detail": f"'{temp_name}' with ID '{series_id}' deleted successfully"}


def update_relationship(db: Session, db_series, field_name: str, related_model, related_data_list: List[str], related_schema: Type[T], **kwargs):
    enums_field = ["genres"]
    logging.info(f"Updating relationship for field: {field_name}")

    current_items = getattr(db_series, field_name)
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
    db.refresh(db_series)
    logging.info(f"Updated {field_name} with new items")
    
    
def update_series(db: Session, series: schema.SeriesUpdate):
    db_series = db.query(Series).filter(Series.id == series.id).first()
    if not db_series:
        return None
    
    update_data = series.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if key not in {"rated", "genres", "stars", "creators", "countries", "languages", "production_companies", "networks"} and value is not None:
            setattr(db_series, key, value)

    relationship_fields = {
        "genres": (Enums, EnumsCreateOrUpdate),
        "stars": (Star, StarCreateOrUpdate),
        "creators": (Creator, CreatorCreateOrUpdate),
        "countries": (Country, CountryCreateOrUpdate),
        "languages": (Language, LanguageCreateOrUpdate),
        "production_companies": (Production, ProductionCreateOrUpdate),
        "networks": (Network, NetworkCreateOrUpdate)
    }
    
    for field, (model, create_or_update) in relationship_fields.items():
        if field in update_data:
            kwargs = {}
            if field in {"genres"}:
                kwargs["site"] = Host._1MDB
                kwargs["type"] = EnumsType.GENRE
            update_relationship(db, db_series, field, model, update_data[field], create_or_update, **kwargs)

    if "rated" in update_data:
        rated_instance = get_or_create(db, Enums, 
                              {
                                  "value" : update_data["rated"].lower(), 
                                  "site":Host._1MDB, "type":EnumsType.RATED
                              }, 
                              url=None)
        if rated_instance:
            db_series.rated = rated_instance
            db_series.rated_id = rated_instance.id
    
    db.commit()
    db.refresh(db_series)
    return db_series