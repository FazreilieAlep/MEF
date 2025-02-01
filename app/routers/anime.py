from app.models.medias.enums_type import EnumsType
from app.models.medias.host import Host
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..models.medias.animes.anime import schema, crud
from ..models.medias import crud as media_crud
from ..models.medias.schema import ItemListResponse, ItemCreate
from typing import Optional, List, Union
from ..core.dependencies.db_dependencies import get_db
from ..core.dependencies.perm_dependencies import permission_required

import logging

router = APIRouter(
    prefix="/anime",
    tags=["anime"],
    responses={404: {"description": "Not found"}},
)

import logging

@router.get("/", response_model=List[schema.AnimeListResponse])
def get_anime_list(
    limit: int = Query(10, ge=1), 
    skip: int = Query(0, ge=0), 
    titles: Optional[List[str]] = Query(None), 
    producers: Optional[List[str]] = Query(None), 
    licensors: Optional[List[str]] = Query(None), 
    studios: Optional[List[str]] = Query(None), 
    genres: Optional[List[str]] = Query(None), 
    types: Optional[List[str]] = Query(None), 
    premiers: Optional[List[str]] = Query(None), 
    db: Session = Depends(get_db)
):
    return crud.get_anime_list(db, limit, skip, titles, producers, licensors, studios, genres, types, premiers)

@router.get("/get_random", response_model=List[schema.AnimeListResponse])
def get_anime_random(
    limit: int = Query(10, ge=1),
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):
    """
    Get anime random anime list 
    """
    return crud.get_anime_random(db, limit, page)

@router.get("/get_by/{item}/{item_id}", response_model=List[schema.AnimeListResponse])
def get_anime_by_item_id(
    item: str,
    item_id: int,
    limit: int = Query(10, ge=1),
    skip: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Get anime list with the specified item_id
    
    **item**: genre OR demographics OR studio OR producer OR licensor OR type OR premier
    **item_id**: integer, id of the item
    """
    valid_items = ['genre', 'demographics', 'studio', 'producer', 'licensor', 'type', 'premier']
    if item not in valid_items:
        raise HTTPException(status_code=400, detail=f"Invalid item. Must be one of {valid_items}")
    
    return crud.get_anime_by_item_id(db, item, item_id, limit, skip)

@router.get("/get/{item}", response_model=Union[List[ItemListResponse], schema.AnimeListResponse])
def get_item_list(
    item: str,
    limit: int = Query(10, ge=1),
    skip: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Get item list with the specified item
    
    **item**: item name -> genre OR studio OR producer OR licensor OR type OR premier
    """
    valid_items = ['genre', 'studio', 'producer', 'licensor', 'type', 'premier']
    if item not in valid_items:
        try:
            anime_id = int(item)
            return crud.get_anime_by_id(db, anime_id)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid item. Must be one of {valid_items} or a valid anime ID")
    
    return crud.get_item_list(db, item, limit, skip)

@router.post("/create/{item}", dependencies=[Depends(permission_required("anime:create"))])
async def create_item(item: str, new_item: ItemCreate, db: Session = Depends(get_db)):
    try:
        """
        Create anime item such as 'genre', 'studio', 'producer', 'licensor', 'type', 'premier'
        
        can be scaled to handle changes in any table or add new db table
        """
        valid_items = ['genre', 'studio', 'producer', 'licensor', 'type', 'premier']
        if item not in valid_items:
            raise HTTPException(status_code=400, detail=f"Invalid item. Must be one of {valid_items}")
       
        # Define additional filter criteria based on item type
        if item == "genre":
            defaults = {"value": new_item.name.lower(), "type": EnumsType.GENRE, "site": Host.MYANIMELIST}
        elif item == "type":
            defaults = {"value": new_item.name.lower(), "type": EnumsType.SHOW_TYPE, "site": Host.MYANIMELIST}
        else:
            defaults = {"name": new_item.name.lower()}

        # Get kwargs data: not filter attributes other than name or value in ItemCreate
        additional_data = {key: value for key, value in new_item.dict().items() if key not in ["name", "value"]}

        # Get item by name with additional filter criteria if applicable
        db_item = media_crud.get_item_by_name(db, item, defaults=defaults)
        
        if db_item:
            raise HTTPException(status_code=400, detail="Item already registered")

        # Create new item
        created_item = media_crud.create_item(db, item, 'anime', item_data=defaults, kwargs=additional_data)
        return created_item

    except Exception as e:
        logging.error(f"Error creating item: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the item.")

@router.post("/create", response_model=schema.Anime, dependencies=[Depends(permission_required("anime:create"))])
async def create_anime(anime: schema.AnimeCreate, db: Session = Depends(get_db)):
    try:
        db_anime = crud.get_anime_by_title(db, title=anime.title_ov)
        if db_anime:
            raise HTTPException(status_code=400, detail="Anime already registered")
        return crud.create_anime(db=db, anime=anime)
    except Exception as e:
        logging.error(f"Error creating anime: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the anime.")

@router.post("/create_bulk", response_model=List[schema.Anime], dependencies=[Depends(permission_required("anime:create"))])
async def create_animes(animes: List[schema.AnimeCreate], db: Session = Depends(get_db)):
    created_animes = []
    for anime in animes:
        try:
            db_anime = crud.get_anime_by_title(db, title=anime.title_ov)
            if db_anime:
                logging.warning(f"Anime '{anime.title_ov}' already registered.")
                created_animes.append(f"Anime '{anime.title_ov}' already registered.")
            else:
                created_anime = crud.create_anime(db=db, anime=anime)
                created_animes.append(created_anime)
        except Exception as e:
            logging.error(f"Error creating anime '{anime.title_ov}': {e}")
    return created_animes
    
@router.put("/update", response_model=schema.Anime, dependencies=[Depends(permission_required("anime:update"))])
def update_anime(anime: schema.AnimeUpdate, db: Session = Depends(get_db)):
    try:
        updated_anime = crud.update_anime(db=db, anime=anime)
        if not updated_anime:
            raise HTTPException(status_code=404, detail="Anime not found")
        return updated_anime
    except Exception as e:
        logging.error(f"Error updating anime: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while updating the anime.")    

@router.put("/update_bulk", response_model=List[schema.Anime], dependencies=[Depends(permission_required("anime:update"))])
async def update_animes(animes: List[schema.AnimeUpdate], db: Session = Depends(get_db)):
    updated_animes = []
    for anime in animes:
        try:
            updated_anime = crud.update_anime(db=db, anime=anime)
            updated_animes.append(updated_anime)
        except Exception as e:
            logging.error(f"Error creating anime '{anime.title_en}': {e}")
    return updated_animes

@router.delete("/delete/{anime_id}", dependencies=[Depends(permission_required("anime:delete"))])
def delete_anime(
    anime_id: int,
    db: Session = Depends(get_db)
):
    return crud.delete_anime(db, anime_id)

@router.delete("/delete/{item}/{id}", dependencies=[Depends(permission_required("anime:delete"))])
def delete_item(
    item: str,
    id: int,
    db: Session = Depends(get_db)
):
    """
    Delete item with the specified item id
    
    **item**: item name -> genre OR studio OR producer OR licensor OR type OR premier
    """
    valid_items = ['genre', 'studio', 'producer', 'licensor', 'type', 'premier']
    if item not in valid_items:
        raise HTTPException(status_code=400, detail=f"Invalid item. Must be one of {valid_items}")

    return media_crud.delete_item(db, item, id, "anime")

@router.delete("/delete_status", dependencies=[Depends(permission_required("anime:delete"))])
def delete_status(
    id: int,
    db: Session = Depends(get_db)
):
    """
    Delete status with the specified status id
    
    **id**: status id
    """
    return crud.delete_status(db, id)

# KIV multiple delete

# KIV: /update/{item}/{item_id}