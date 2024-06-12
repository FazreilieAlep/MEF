# Store medias global functions

from fastapi import HTTPException
from typing import Type, TypeVar, Dict, Any, Union
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional

from .enums.enums import Enums
from .enums_type import EnumsType
from .host import Host
from .star.star import Star
from .country.country import Country
from .language.language import Language
from .movies.director.director import Director
from .series.creator.creator import Creator
from .series.network.network import Network
from .series.production.production import Production
from .animes.producer.producer import Producer
from .animes.licensor.licensor import Licensor
from .animes.studio.studio import Studio
from .animes.premier.premier import Premier


T = TypeVar('T', bound=DeclarativeMeta)

def get_or_create(db: Session, model: Type[T], defaults: Dict[str, Any], **kwargs) -> Union[T, None]:
    """
    Get or create a model object based on the provided data.

    Args:
        db (Session): SQLAlchemy database session.
        model (Type[T]): Model class to create the object.
        defaults (Dict[str, Any]): Dictionary containing default values for object creation.
        **kwargs: Additional keyword arguments representing additional fields for object creation.

    Returns:
        Union[T, None]: The created or existing object.
    """
    # Use only defaults for filtering criteria
    filter_criteria = {key: value for key, value in defaults.items()}
    
    # Filter out kwargs that match the model's column names
    model_columns = model.__table__.columns.keys()
    additional_data = {key: value for key, value in kwargs.items() if key in model_columns}
    
    # Create a query with the filter criteria
    instance = db.query(model).filter_by(**filter_criteria).first()
    
    if not instance:
        # Create new object with defaults and additional kwargs without using .update
        new_data = {**defaults, **additional_data}
        instance = model(**new_data)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        
    return instance

def get_or_create_direct(db: Session, model: Type[T], **kwargs) -> Union[T, None]:
    try:
        instance = db.query(model).filter_by(**kwargs).first()
        if not instance:
            instance = model(**kwargs)
            db.add(instance)
            db.commit()
            db.refresh(instance)
        return instance
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error creating or getting {model.__name__}: {e}")
        return None
    

def delete_item(db: Session, item: str, id: int, content_type: str):
    # Define mappings of items to their corresponding model classes and related fields
    item_models = {
        'movie': {
            'genre': (Enums, EnumsType.GENRE, Host._1MDB, 'genre_movies'),
            'rated': (Enums, EnumsType.RATED, Host._1MDB, 'rated_movies'),
            'star': (Star, None, None, 'movies'),
            'director': (Director, None, None, 'movies'),
            'country': (Country, None, None, 'movies'),
            'language': (Language, None, None, 'movies'),
        },
        'series': {
            'genre': (Enums, EnumsType.GENRE, Host._1MDB, 'genre_series'),
            'rated': (Enums, EnumsType.RATED, Host._1MDB, 'rated_series'),
            'star': (Star, None, None, 'series'),
            'creator': (Creator, None, None, 'series'),
            'country': (Country, None, None, 'series'),
            'language': (Language, None, None, 'series'),
            'production': (Production, None, None, 'series'),
            'network': (Network, None, None, 'series'),
        },
        'anime': {
            'genre': (Enums, EnumsType.GENRE, Host.MYANIMELIST, 'genre_animes'),
            'demographics': (Enums, EnumsType.GENRE, Host.MYANIMELIST, 'genre_animes'),
            'studio': (Studio, None, None, 'created'),
            'producer': (Producer, None, None, 'produced'),
            'licensor': (Licensor, None, None, 'licensed'),
            'type': (Enums, EnumsType.SHOW_TYPE, Host.MYANIMELIST, 'type_animes'),
            'premier': (Premier, None, None, 'anime')
        }
    }

    if content_type not in item_models or item not in item_models[content_type]:
        raise HTTPException(status_code=400, detail="Invalid content type or item type")

    Model, enum_type, site, related_field = item_models[content_type][item]

    # Query the item based on the provided parameters
    db_item = db.query(Model).filter(Model.id == id)
    if enum_type is not None:
        db_item = db_item.filter(Model.type == enum_type, Model.site == site)
    db_item = db_item.first()

    if not db_item:
        raise HTTPException(status_code=404, detail=f"{item.capitalize()} with ID {id} not found")

    # Check if the item is related to any content before deletion
    if getattr(db_item, related_field):
        raise HTTPException(status_code=400, detail=f"Cannot delete {item} because it is still related to a {content_type}.")

    # Delete the item and commit the transaction
    db.delete(db_item)
    db.commit()
    return {"detail": f"{item.capitalize()} with ID {id} deleted successfully"}

def get_item_by_name(db: Session, item: str, defaults: Dict[str, Any]) -> Optional[Any]:
    """
    Get an item by its name.

    Args:
        db (Session): SQLAlchemy database session.
        item (str): The type of item to query.
        defaults (Dict[str, Any]): Additional filter criteria.

    Returns:
        The queried item or None if not found.
    """
    item_models = {
        'genre': Enums,
        'rated': Enums,
        'star': Star,
        'director': Director,
        'country': Country,
        'language': Language,
        'creator': Creator,
        'production': Production,
        'network': Network,
        'studio': Studio,
        'producer': Producer,
        'licensor': Licensor,
        'type': Enums,
        'premier': Premier
    }
    
    if item not in item_models:
        raise ValueError("Invalid item type")

    Model = item_models[item]

    return db.query(Model).filter_by(**defaults).first()

def create_item(db: Session, item: str, content_type: str, item_data: Dict[str, Any], kwargs: Dict[str, Any]) -> Dict[str, Any]:
    # Define mappings of items to their corresponding model classes and additional fields
    item_models = {
        'movie': {
            'genre': Enums,
            'rated': Enums,
            'star': Star,
            'director': Director,
            'country': Country,
            'language': Language,
        },
        'series': {
            'genre': Enums,
            'rated': Enums,
            'star': Star,
            'creator': Creator,
            'country': Country,
            'language': Language,
            'production': Production,
            'network': Network,
        },
        'anime': {
            'genre': Enums,
            'studio': Studio,
            'producer': Producer,
            'licensor': Licensor,
            'type': Enums,
            'premier': Premier,
        }
    }

    if content_type not in item_models or item not in item_models[content_type]:
        raise HTTPException(status_code=400, detail="Invalid content type or item type")

    Model = item_models[content_type][item]

    instance = get_or_create(db, Model, item_data, **kwargs)
    if instance:
        return {"detail": f"new {item.capitalize()} for {content_type} created successfully or already exists", "created": instance}
    else:
        raise HTTPException(status_code=500, detail="Failed to create the item")