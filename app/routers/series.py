from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.models.medias.enums_type import EnumsType
from app.models.medias.host import Host
from ..models.medias.series.series import schema, crud
from ..models.medias import crud as media_crud
from ..models.medias.schema import ItemListResponse, ItemCreate
from typing import Optional
from ..core.dependencies.db_dependencies import get_db
from ..core.dependencies.perm_dependencies import permission_required

import logging
from typing import List

router = APIRouter(
    prefix="/series",
    tags=["series"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[schema.SeriesListResponse])
def get_series_list(
    limit: int = Query(10, ge=1), 
    skip: int = Query(0, ge=0), 
    titles: Optional[List[str]] = Query(None), 
    genres: Optional[List[str]] = Query(None), 
    stars: Optional[List[str]] = Query(None), 
    creators: Optional[List[str]] = Query(None), 
    countries: Optional[List[str]] = Query(None), 
    languages: Optional[List[str]] = Query(None), 
    productions: Optional[List[str]] = Query(None), 
    networks: Optional[List[str]] = Query(None), 
    db: Session = Depends(get_db)
):
    return crud.get_series_list(db, limit, skip, titles, genres, stars, creators, countries, languages, productions, networks)

@router.get("/get_by/{item}/{item_id}", response_model=List[schema.SeriesListResponse])
def get_series_by_item_id(
    item: str,
    item_id: int,
    limit: int = Query(10, ge=1),
    skip: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    valid_items = ['genre', 'rated', 'star', 'creator', 'country', 'language', 'production', 'network']
    if item not in valid_items:
        raise HTTPException(status_code=400, detail=f"Invalid item. Must be one of {valid_items}")
    
    return crud.get_series_by_item_id(db, item, item_id, limit, skip)

@router.get("/get/{item}", response_model=List[ItemListResponse])
def get_item_list(
    item: str,
    limit: int = Query(10, ge=1),
    skip: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    valid_items = ['genre', 'rated', 'star', 'creator', 'country', 'language', 'production', 'network']
    if item not in valid_items:
        raise HTTPException(status_code=400, detail=f"Invalid item. Must be one of {valid_items}")
    
    return crud.get_item_list(db, item, limit, skip)

@router.post("/create/{item}", dependencies=[Depends(permission_required("series:create"))])
async def create_item(item: str, new_item: ItemCreate, db: Session = Depends(get_db)):
    try:
        """
        Create anime item such as 'genre', 'rated', 'star', 'creator', 'country', 'language', 'production', 'network'
        
        can be scaled to handle changes in any table or add new db table
        """
        valid_items = ['genre', 'rated', 'star', 'creator', 'country', 'language', 'production', 'network']
        if item not in valid_items:
            raise HTTPException(status_code=400, detail=f"Invalid item. Must be one of {valid_items}")
       
        # Define additional filter criteria based on item type
        if item == "genre":
            defaults = {"value": new_item.name.lower(), "type": EnumsType.GENRE, "site": Host._1MDB}
        elif item == "rated":
            defaults = {"value": new_item.name.lower(), "type": EnumsType.RATED, "site": Host._1MDB}
        else:
            defaults = {"name": new_item.name.lower()}

        # Get kwargs data: not filter attributes other than name or value in ItemCreate
        additional_data = {key: value for key, value in new_item.dict().items() if key not in ["name", "value"]}

        # Get item by name with additional filter criteria if applicable
        db_item = media_crud.get_item_by_name(db, item, defaults=defaults)
        
        if db_item:
            raise HTTPException(status_code=400, detail="Item already registered")

        # Create new item
        created_item = media_crud.create_item(db, item, 'series', item_data=defaults, kwargs=additional_data)
        return created_item

    except Exception as e:
        logging.error(f"Error creating item: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the item.")

@router.post("/create", response_model=schema.Series, dependencies=[Depends(permission_required("series:create"))])
async def create_series(series: schema.SeriesCreate, db: Session = Depends(get_db)):
    try:
        db_series = crud.get_series_by_title(db, title=series.title)
        if db_series:
            raise HTTPException(status_code=400, detail="series already registered")
        return crud.create_series(db=db, series=series)
    except Exception as e:
        logging.error(f"Error creating series: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the series.")

@router.post("/create_bulk", response_model=List[schema.Series], dependencies=[Depends(permission_required("series:create"))])
async def create_serieses(serieses: List[schema.SeriesCreate], db: Session = Depends(get_db)):
    created_serieses = []
    for series in serieses:
        try:
            db_series = crud.get_series_by_title(db, title=series.title)
            if db_series:
                logging.warning(f"Anime '{series.title}' already registered.")
                created_serieses.append(f"Anime '{series.title}' already registered.")
            else:
                created_series = crud.create_series(db=db, series=series)
                created_serieses.append(created_series)
        except Exception as e:
            logging.error(f"Error creating anime '{series.title}': {e}")
    return created_serieses

@router.delete("/delete/{series_id}", dependencies=[Depends(permission_required("series:delete"))])
def delete_series_route(
    series_id: str,
    db: Session = Depends(get_db)
):
    return crud.delete_series(db, series_id)

@router.delete("/delete/{item}/{id}", dependencies=[Depends(permission_required("series:delete"))])
def delete_item(
    item: str,
    id: int,
    db: Session = Depends(get_db)
):
    valid_items = ['genre', 'rated', 'star', 'creator', 'country', 'language', 'production', 'network']
    if item not in valid_items:
        raise HTTPException(status_code=400, detail=f"Invalid item. Must be one of {valid_items}")
    return media_crud.delete_item(db, item, id, "series")

@router.put("/update", response_model=schema.Series, dependencies=[Depends(permission_required("series:update"))])
def update_series(series: schema.SeriesUpdate, db: Session = Depends(get_db)):
    try:
        updated_series = crud.update_series(db=db, series=series)
        if not updated_series:
            raise HTTPException(status_code=404, detail="series not found")
        return updated_series
    except Exception as e:
        logging.error(f"Error updating series: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while updating the series.")

@router.put("/update/multiple", response_model=List[schema.Series], dependencies=[Depends(permission_required("series:update"))])
async def update_seriess(seriess: List[schema.SeriesUpdate], db: Session = Depends(get_db)):
    updated_seriess = []
    for series in seriess:
        try:
            updated_series = crud.update_series(db=db, series=series)
            updated_seriess.append(updated_series)
        except Exception as e:
            logging.error(f"Error creating series '{series.title}': {e}")
    return updated_seriess

# KIV: /update/{item}/{item_id}