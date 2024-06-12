from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.models.medias.enums_type import EnumsType
from app.models.medias.host import Host
from ..models.medias.movies.movie import schema, crud
from ..models.medias import crud as media_crud
from ..models.medias.schema import ItemListResponse, ItemCreate
from typing import Optional
from ..core.dependencies.db_dependencies import get_db
from ..core.dependencies.perm_dependencies import permission_required

import logging
from typing import List

router = APIRouter(
    prefix="/movie",
    tags=["movie"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[schema.MovieListResponse])
def get_movie_list(
    limit: int = Query(10, ge=1), 
    skip: int = Query(0, ge=0), 
    titles: Optional[List[str]] = Query(None), 
    genres: Optional[List[str]] = Query(None), 
    stars: Optional[List[str]] = Query(None), 
    directors: Optional[List[str]] = Query(None), 
    countries: Optional[List[str]] = Query(None), 
    languages: Optional[List[str]] = Query(None), 
    db: Session = Depends(get_db)
):
    return crud.get_movie_list(db, limit, skip, titles, genres, stars, directors, countries, languages)

@router.get("/{item}/{item_id}", response_model=List[schema.MovieListResponse])
def get_movie_by_item_id(
    item: str,
    item_id: int,
    limit: int = Query(10, ge=1),
    skip: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Get movie list with the specified item id
    
    **item**: item name -> genre OR rated OR star OR director OR country OR language
    **item_id**: integer, id of the item
    """
    valid_items = ['genre', 'rated', 'star', 'director', 'country', 'language']
    if item not in valid_items:
        raise HTTPException(status_code=400, detail=f"Invalid item. Must be one of {valid_items}")
    
    return crud.get_movie_by_item_id(db, item, item_id, limit, skip)

@router.get("/{item}", response_model=List[ItemListResponse])
def get_item_list(
    item: str,
    limit: int = Query(10, ge=1),
    skip: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Get item list with the specified item
    
    **item**: item name -> genre OR rated OR star OR director OR country OR language
    """
    valid_items = ['genre', 'rated', 'star', 'director', 'country', 'language']
    if item not in valid_items:
        raise HTTPException(status_code=400, detail=f"Invalid item. Must be one of {valid_items}")
    
    return crud.get_item_list(db, item, limit, skip)

@router.post("/{item}", dependencies=[Depends(permission_required("movie:create"))])
async def create_item(item: str, new_item: ItemCreate, db: Session = Depends(get_db)):
    try:
        """
        Create anime item such as 'genre', 'rated', 'star', 'director', 'country', 'language'
        
        can be scaled to handle changes in any table or add new db table
        """
        valid_items = ['genre', 'rated', 'star', 'director', 'country', 'language']
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
        created_item = media_crud.create_item(db, item, 'movie', item_data=defaults, kwargs=additional_data)
        return created_item
    
    except Exception as e:
        logging.error(f"Error creating item: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the item.")

@router.post("/", response_model=schema.Movie, dependencies=[Depends(permission_required("movie:create"))])
async def create_movie(movie: schema.MovieCreate, db: Session = Depends(get_db)):
    try:
        db_movie = crud.get_movie_by_title(db, title=movie.title)
        if db_movie:
            raise HTTPException(status_code=400, detail="movie already registered")
        return crud.create_movie(db=db, movie=movie)
    except Exception as e:
        logging.error(f"Error creating movie: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the movie.")

@router.post("/multiple", response_model=List[schema.Movie], dependencies=[Depends(permission_required("movie:create"))])
async def create_movies(movies: List[schema.MovieCreate], db: Session = Depends(get_db)):
    created_movies = []
    for movie in movies:
        try:
            db_movie = crud.get_movie_by_title(db, title=movie.title)
            if db_movie:
                logging.warning(f"movie '{movie.title}' already registered.")
            else:
                created_movie = crud.create_movie(db=db, movie=movie)
                created_movies.append(created_movie)
        except Exception as e:
            logging.error(f"Error creating movie '{movie.title}': {e}")
    return created_movies

@router.delete("/delete/{movie_id}", dependencies=[Depends(permission_required("movie:delete"))])
def delete_movie_route(
    movie_id: str,
    db: Session = Depends(get_db)
):
    return crud.delete_movie(db, movie_id)

@router.delete("/delete/{item}/{id}", dependencies=[Depends(permission_required("movie:delete"))])
def delete_item(
    item: str,
    id: int,
    db: Session = Depends(get_db)
):
    valid_items = ['genre', 'rated', 'star', 'director', 'country', 'language']
    if item not in valid_items:
        raise HTTPException(status_code=400, detail=f"Invalid item. Must be one of {valid_items}")
    return media_crud.delete_item(db, item, id, "movie")

@router.put("/update", response_model=schema.Movie, dependencies=[Depends(permission_required("movie:update"))])
def update_movie(movie: schema.MovieUpdate, db: Session = Depends(get_db)):
    try:
        updated_movie = crud.update_movie(db=db, movie=movie)
        if not updated_movie:
            raise HTTPException(status_code=404, detail="movie not found")
        return updated_movie
    except Exception as e:
        logging.error(f"Error updating movie: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while updating the movie.")

@router.put("/update/multiple", response_model=List[schema.Movie], dependencies=[Depends(permission_required("movie:update"))])
async def update_movies(movies: List[schema.MovieUpdate], db: Session = Depends(get_db)):
    updated_movies = []
    for movie in movies:
        try:
            updated_movie = crud.update_movie(db=db, movie=movie)
            updated_movies.append(updated_movie)
        except Exception as e:
            logging.error(f"Error creating movie '{movie.title}': {e}")
    return updated_movies