from http.client import HTTPException
from fastapi import Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
import logging

# main object import
from .anime import Anime
from ..licensor.licensor import Licensor
from ..producer.producer import Producer
from ..studio.studio import Studio
from ..premier.premier import Premier
from ...enums.enums import Enums
from ..alternative_titles.alternative_titles import Alternative_Titles
from . import schema

# related object import
from ..information.crud import create_anime_information, update_anime_information

# enums
from ....medias.enums_type import EnumsType
from ....medias.host import Host
from sqlalchemy.ext.declarative import DeclarativeMeta
from typing import Type, TypeVar, Dict, Any, Optional, List

# schema
from ..licensor.schema import LicensorCreateOrUpdate
from ..producer.schema import ProducerCreateOrUpdate
from ..studio.schema import StudioCreateOrUpdate
from ...enums.schema import EnumsCreateOrUpdate

from ...crud import get_or_create

T = TypeVar('T', bound=DeclarativeMeta)
BaseModel = TypeVar('BaseModel')

logging.basicConfig(level=logging.INFO)

def get_anime_by_title(db: Session, title: str):
    return db.query(Anime).filter(Anime.title_ov == title.lower()).first()

def get_anime_list(
    db: Session, 
    limit: int, 
    skip: int, 
    titles: Optional[List[str]] = None, 
    producers: Optional[List[str]] = None, 
    licensors: Optional[List[str]] = None, 
    studios: Optional[List[str]] = None, 
    genres: Optional[List[str]] = None, 
    types: Optional[List[str]] = None, 
    premiers: Optional[List[str]] = None,
):
    query = db.query(Anime)

    if titles:
        titles = [title.lower() for title in titles]
        title_en_conditions = [Anime.title_en.ilike(f"%{title}%") for title in titles]
        title_ov_conditions = [Anime.title_ov.ilike(f"%{title}%") for title in titles]
        query = query.join(Alternative_Titles, isouter=True)
        synonym_conditions = [Alternative_Titles.synonym.ilike(f"%{title}%") for title in titles]
        query = query.filter(
            or_(
                *title_en_conditions,
                *title_ov_conditions,
                *synonym_conditions
            )
        )

    if genres:
        genres = [genre.lower() for genre in genres]
        genre_conditions = [Enums.value.ilike(f"%{genre}%") for genre in genres]
        query = query.filter(Anime.genres.any(or_(*genre_conditions)))

    if producers:
        producers = [producer.lower() for producer in producers]
        producer_conditions = [Producer.name.ilike(f"%{producer}%") for producer in producers]
        query = query.filter(Anime.producers.any(or_(*producer_conditions)))

    if licensors:
        licensors = [licensor.lower() for licensor in licensors]
        licensor_conditions = [Licensor.name.ilike(f"%{licensor}%") for licensor in licensors]
        query = query.filter(Anime.licensors.any(or_(*licensor_conditions)))

    if studios:
        studios = [studio.lower() for studio in studios]
        studio_conditions = [Studio.name.ilike(f"%{studio}%") for studio in studios]
        query = query.filter(Anime.studios.any(or_(*studio_conditions)))

    if types:
        types = [type.lower() for type in types]
        type_conditions = [Enums.value.ilike(f"%{type}%") for type in types]
        query = query.filter(Anime.type.has(or_(*type_conditions)))
        
    if premiers:
        premiers = [premier.lower() for premier in premiers]
        premier_conditions = [Premier.name.ilike(f"%{premier}%") for premier in premiers]
        query = query.filter(Anime.premiered.has(or_(*premier_conditions)))

    return query.offset(skip).limit(limit).all()


def get_anime_by_genre_id(db: Session, genre_id: int, limit: int, skip: int) -> List[Anime]:
    return db.query(Anime).join(Enums, Anime.genres).filter(
        Enums.id == genre_id,
        Enums.site == Host.MYANIMELIST,
        Enums.type == EnumsType.GENRE
    ).offset(skip).limit(limit).all()

def get_anime_by_studio_id(db: Session, studio_id: int, limit: int, skip: int) -> List[Anime]:
    return db.query(Anime).join(Studio, Anime.studios).filter(
        Studio.id == studio_id
    ).offset(skip).limit(limit).all()

def get_anime_by_producer_id(db: Session, producer_id: int, limit: int, skip: int) -> List[Anime]:
    return db.query(Anime).join(Producer, Anime.studios).filter(
        Producer.id == producer_id
    ).offset(skip).limit(limit).all()

def get_anime_by_item_id(db: Session, item: str, item_id: int, limit: int, skip: int) -> List[Anime]:
    query = db.query(Anime)
    
    if item == 'genre' or item == 'demographic':
        query = query.join(Enums, Anime.genres).filter(
            Enums.id == item_id,
            Enums.site == Host.MYANIMELIST,
            Enums.type == EnumsType.GENRE
        )
    elif item == 'demographics':
        query = query.join(Enums, Anime.demographics).filter(
            Enums.id == item_id,
            Enums.site == Host.MYANIMELIST,
            Enums.type == EnumsType.GENRE
        )
    elif item == 'studio':
        query = query.join(Studio, Anime.studios).filter(Studio.id == item_id)
    elif item == 'producer':
        query = query.join(Producer, Anime.producers).filter(Producer.id == item_id)
    elif item == 'licensor':
        query = query.join(Licensor, Anime.licensors).filter(Licensor.id == item_id)
    elif item == 'type':
        query = query.filter(Anime.type_id == item_id)
    elif item == 'premier':
        query = query.filter(Anime.premier_id == item_id)
    
    return query.offset(skip).limit(limit).all()

def get_item_list(db: Session, item: str, limit: int, skip: int) -> List:
    if item == 'genre':
        return db.query(Enums).filter(
            Enums.site == Host.MYANIMELIST, 
            Enums.type == EnumsType.GENRE).offset(skip).limit(limit).all()
    elif item == 'studio':
        return db.query(Studio).offset(skip).limit(limit).all()
    elif item == 'producer':
        return db.query(Producer).offset(skip).limit(limit).all()
    elif item == 'licensor':
        return db.query(Licensor).offset(skip).limit(limit).all()
    elif item == 'type':
        return db.query(Enums).filter(
            Enums.site == Host.MYANIMELIST, 
            Enums.type == EnumsType.SHOW_TYPE).offset(skip).limit(limit).all()
    elif item == 'premier':
        return db.query(Premier).offset(skip).limit(limit).all()
    return []

# Optimal create_anime function code
def create_anime(db: Session, anime=schema.AnimeCreate):
    
    # Create or get related objects
    type = get_or_create(db, Enums, {
        "value" : anime.type.name.lower(), 
        "site" : Host.MYANIMELIST, 
        "type" : EnumsType.SHOW_TYPE
        }, url = str(anime.type.url)) if anime.type else None
    
    genres = [get_or_create(db, Enums, {
        "value" : genre.name.lower(), 
        "site" :  Host.MYANIMELIST, 
        "type" : EnumsType.GENRE 
        }, url = str(genre.url)) for genre in anime.genres] if anime.genres else []
    
    demographics = [get_or_create(db, Enums, {
        "value" : anime.type.name.lower(),
        "site" : Host.MYANIMELIST, 
        "type" : EnumsType.GENRE
        }, url = str(anime.type.url)) for demographic in anime.demographics] if anime.demographics else []
  
    premiered = get_or_create(db, Premier, {"name" : anime.premiered.name.lower()}, url = str(anime.premiered.url) ) if anime.premiered else None
    producers = [get_or_create(db, Producer, {"name" : producer.name.lower()}, url = str(producer.url) ) for producer in anime.producers] if anime.producers else []
    licensors = [get_or_create(db, Licensor, {"name" : licensor.name.lower()}, url = str(licensor.url) ) for licensor in anime.licensors] if anime.licensors else []
    studios = [get_or_create(db, Studio, {"name" : studio.name.lower()}, url = str(studio.url) ) for studio in anime.studios] if anime.studios else []
    
    # Create main Anime object
    db_anime = get_anime_by_title(db, anime.title_en)
    if db_anime is None:
        db_anime = Anime(
            id=anime.id, # This can be None; SQLAlchemy will auto-generate if None
            title_ov=anime.title_ov.lower() if anime.title_ov else None,
            title_en=anime.title_en.lower() if anime.title_en else None,
            synopsis=anime.synopsis,
            picture_url=str(anime.picture_url),
            type_id=type.id if type else None,
            premier_id=premiered.id if premiered else None,
        )
  
        # Add to session
        db.add(db_anime)
        db.commit()
        db.refresh(db_anime)
     # Create and associate related objects
    alternative_titles = get_or_create(db,
                                       Alternative_Titles, 
                                       {"anime_id" : db_anime.id}, 
                                       japanese=anime.alternative_titles.japanese, 
                                       synonym=anime.alternative_titles.synonym.lower() if anime.alternative_titles.synonym else None) if anime.alternative_titles else None
    information = create_anime_information(db, anime.information, db_anime.id) if anime.information else None
    db_anime.alternative_titles = alternative_titles
    db_anime.information = information
    db_anime.producers = producers
    db_anime.licensors = licensors
    db_anime.studios = studios
    db_anime.genres = genres
    db_anime.demographics = demographics
    db_anime.premiered = premiered
    db_anime.type = type
    db.commit()
    db.refresh(db_anime)
    
    return db_anime

def update_relationship(db: Session, db_anime, field_name: str, related_model, related_data_list: List[Dict[str, Any]], related_schema: Type[T], **kwargs):
    enums_field = ["genres", "demographics"]
    logging.info(f"Updating relationship for field: {field_name}")

    current_items = getattr(db_anime, field_name)
    current_items_dict = {item.id: item for item in current_items}

    new_items = []
    for item_data in related_data_list:
        item_id = item_data.get("id")
        item_name = item_data.get("name").lower() if item_data.get("name") else None

        if item_id:
            if field_name not in enums_field:
                item = get_or_create(db, related_model, {"id" : item_id})
            else:
                item = get_or_create(db, related_model, {"id" : item_id}, value=item_name, **kwargs)
        elif item_name:
            if field_name not in enums_field:
                item = get_or_create(db, related_model, {"name" : item_name})
            else:
                item = get_or_create(db, related_model, {"value" : item_name}, **kwargs)
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
    db.refresh(db_anime)
    logging.info(f"Updated {field_name} with new items")

# Optimized update_anime
def update_anime(db: Session, anime: schema.AnimeUpdate):
    db_anime = db.query(Anime).filter(Anime.id == anime.id).first()
    if not db_anime:
        return None
    
    update_data = anime.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        if key not in {"alternative_titles", "information", "producers", "licensors", "studios", "genres", "demographics", "type", "premiered"} and value is not None:
            setattr(db_anime, key, value)
    
    relationship_fields = {
        "producers": (Producer, ProducerCreateOrUpdate),
        "licensors": (Licensor, LicensorCreateOrUpdate),
        "studios": (Studio, StudioCreateOrUpdate),
        "genres": (Enums, EnumsCreateOrUpdate),
        "demographics": (Enums, EnumsCreateOrUpdate)
    }
    
    for field, (model, create_or_update) in relationship_fields.items():
        if field in update_data:
            kwargs = {}
            if field in {"genres", "demographics"}:
                kwargs["site"] = Host.MYANIMELIST
                kwargs["type"] = EnumsType.GENRE
            update_relationship(db, db_anime, field, model, update_data[field], create_or_update, **kwargs)

    if "type" in update_data:
        type_instance = get_or_create(db, Enums, 
                                      {
                                          "value" : update_data["type"]["name"].lower(), 
                                          "site":Host.MYANIMELIST, "type":EnumsType.SHOW_TYPE
                                      }, 
                                      url=str(update_data["type"].get("url")) if update_data["type"].get("url") else None)
        if type_instance:
            db_anime.type = type_instance

    if "premiered" in update_data:
        premiered_instance = get_or_create(db, Premier,
                                           {
                                               "name":update_data["premiered"]["name"].lower()
                                           },
                                           url=str(update_data["premiered"].get("url")) if update_data["premiered"].get("url") else None)
        if premiered_instance:
            db_anime.premiered = premiered_instance

    if "alternative_titles" in update_data:
        alternative_titles_data = update_data["alternative_titles"]
        if not db_anime.alternative_titles:
            db_anime.alternative_titles = Alternative_Titles(anime_id=db_anime.id)
        db_anime.alternative_titles.synonym = alternative_titles_data.get("synonym", db_anime.alternative_titles.synonym).lower()
        db_anime.alternative_titles.japanese = alternative_titles_data.get("japanese", db_anime.alternative_titles.japanese)
                
    if "information" in update_data:
        db_anime.information = update_anime_information(db, anime.information, db_anime)
    
    db.commit()
    db.refresh(db_anime)
    return db_anime

def delete_status(db: Session, id: int):
    status = db.query(Enums).filter(Enums.id == id, Enums.type == EnumsType.STATUS, Enums.site == Host.MYANIMELIST).first()
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    db.delete(status)
    db.commit()
    
def delete_anime(db: Session, anime_id: int):
    anime = db.query(Anime).filter(Anime.id == anime_id).first()
    temp_name = anime.title_en
    if not anime:
        raise HTTPException(status_code=404, detail="Anime not found")
    db.delete(anime)
    db.commit()
    return {"detail": f"{temp_name} with ID {anime_id} deleted successfully"}


# Original create_anime function code
# def create_anime(db: Session, anime=schema.AnimeCreate):
    
#     # Create or get related objects
#     type = get_or_create_enum(db, anime.type, Host.MYANIMELIST, EnumsType.SHOW_TYPE) if anime.type else None
#     genres = [get_or_create_enum(db, genre, Host.MYANIMELIST, EnumsType.GENRE) for genre in anime.genres] if anime.genres else []
#     demographics = [get_or_create_enum(db, demographic, Host.MYANIMELIST, EnumsType.GENRE) for demographic in anime.demographics] if anime.demographics else []
  
#     premiered = get_or_create_premier(db, anime.premiered) if anime.premiered else None
#     producers = [get_or_create_producer(db, producer) for producer in anime.producers] if anime.producers else []
#     licensors = [get_or_create_licensor(db, licensor) for licensor in anime.licensors] if anime.licensors else []
#     studios = [get_or_create_studio(db, studio) for studio in anime.studios] if anime.studios else []
    
#     # Create main Anime object
#     db_anime = get_anime_by_title(db, anime.title_en)
#     if db_anime is None:
#         db_anime = Anime(
#             id=anime.id, # This can be None; SQLAlchemy will auto-generate if None
#             title_ov=anime.title_ov,
#             title_en=anime.title_en,
#             synopsis=anime.synopsis,
#             picture_url=str(anime.picture_url),
#             type_id=type.id if type else None,
#             premier_id=premiered.id if premiered else None,
#         )
  
#         # Add to session
#         db.add(db_anime)
#         db.commit()
#         db.refresh(db_anime)
#      # Create and associate related objects
#     alternative_titles = get_or_create_alt_title(db, anime.alternative_titles, db_anime.id) if anime.alternative_titles else None
#     information = create_anime_information(db, anime.information, db_anime.id) if anime.information else None
#     db_anime.alternative_titles = alternative_titles
#     db_anime.information = information
#     db_anime.producers = producers
#     db_anime.licensors = licensors
#     db_anime.studios = studios
#     db_anime.genres = genres
#     db_anime.demographics = demographics
#     db_anime.premiered = premiered
#     db_anime.type = type
#     db.commit()
#     db.refresh(db_anime)
    
#     return db_anime


# Original update_anime
# def update_anime(db: Session, anime: schema.AnimeUpdate):
#     db_anime = db.query(Anime).filter(Anime.id == anime.id).first()
#     if not db_anime:
#         return None
    
#     update_data = anime.dict(exclude_unset=True)
    
#     for key, value in update_data.items():
#         if key not in ["alternative_titles", "information", "producers", "licensors", "studios", "genres", "demographics", "type", "premiered"] and value is not None:
#             setattr(db_anime, key, value)
    
#     if "producers" in update_data:
#         update_relationship(db, db_anime, 'producers', Producer, update_data["producers"], ProducerCreateOrUpdate)

#     if "licensors" in update_data:
#         update_relationship(db, db_anime, 'licensors', Licensor, update_data["licensors"], LicensorCreateOrUpdate)

#     if "studios" in update_data:
#         update_relationship(db, db_anime, 'studios', Studio, update_data["studios"], StudioCreateOrUpdate)

#     if "genres" in update_data:
#         update_relationship(db, db_anime, 'genres', Enums, update_data["genres"], EnumsCreateOrUpdate, site=Host.MYANIMELIST, type=EnumsType.GENRE)

#     if "demographics" in update_data:
#         update_relationship(db, db_anime, 'demographics', Enums, update_data["demographics"], EnumsCreateOrUpdate, site=Host.MYANIMELIST, type=EnumsType.GENRE)

#     if "type" in update_data:
#         type_instance = get_or_create(db, Enums, update_data["type"], site=Host.MYANIMELIST, type=EnumsType.SHOW_TYPE)
#         if type_instance:
#             db_anime.type = type_instance

#     if "premiered" in update_data:
#         premiered_instance = get_or_create(db, Premier, update_data["premiered"])
#         if premiered_instance:
#             db_anime.premiered = premiered_instance

#     if "alternative_titles" in update_data:
#         if not db_anime.alternative_titles:
#             db_anime.alternative_titles = Alternative_Titles(anime_id=db_anime.id)
        
#         alternative_titles_data = update_data["alternative_titles"]
        
#         if "synonym" in alternative_titles_data:
#             db_anime.alternative_titles.synonym = alternative_titles_data["synonym"].lower()
        
#         if "japanese" in alternative_titles_data:
#             db_anime.alternative_titles.japanese = alternative_titles_data["japanese"]
                
#     if "information" in update_data:
#         db_anime.information = update_anime_information(db, anime.information, db_anime)
    
#     db.commit()
#     db.refresh(db_anime)
#     db.refresh(db_anime)
#     return db_anime

# Original delele_item
# def delete_item(db: Session, item: str, id: int):
#     try:
#         if item == 'genre' or item == 'demographics':
#             genre = db.query(Enums).filter(Enums.id == id, Enums.type == EnumsType.GENRE, Enums.site == Host.MYANIMELIST).first()
#             if genre and not genre.genre_animes:
#                 db.delete(genre)
#         elif item == 'studio':
#             studio = db.query(Studio).filter(Studio.id == id).first()
#             if studio and not studio.created:
#                 db.delete(studio)
#         elif item == 'producer':
#             producer = db.query(Producer).filter(Producer.id == id).first()
#             if producer and not producer.produced:
#                 db.delete(producer)
#         elif item == 'licensor':
#             licensor = db.query(Licensor).filter(Licensor.id == id).first()
#             if licensor and not licensor.licensed:
#                 db.delete(licensor)
#         elif item == 'type':
#             show_type = db.query(Enums).filter(Enums.id == id, Enums.type == EnumsType.SHOW_TYPE, Enums.site == Host.MYANIMELIST).first()
#             if show_type and not show_type.type_animes:
#                 db.delete(show_type)
#         elif item == 'premier':
#             premier = db.query(Premier).filter(Premier.id == id).first()
#             if premier and not premier.anime:
#                 db.delete(premier)

#         db.commit()
#         return {"detail": f"{item.capitalize()} with ID {id} deleted successfully"}

#     except IntegrityError:
#         db.rollback()
#         raise HTTPException(status_code=400, detail="Cannot delete item because it is still related to an anime.")

#     return {"detail": f"{item.capitalize()} with ID {id} is still related to existing anime"}