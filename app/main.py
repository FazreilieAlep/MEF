import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from .routers import users, anime, movies, series
from typing_extensions import Annotated
from .core.dependencies.auth_dependencies import get_current_active_user
from .core.dependencies.db_dependencies import get_db
from .models.users.schema import CurrentUser
from .models.users.crud import get_user_login

description = """
MEF API is designed to manage media or content data such as movies, series, and anime details, specifically tailored to track the media content you have personally watched.

## Features

### Object Relational Mapping (ORM)
- Utilizes [SQLAlchemy](https://www.sqlalchemy.org/) for PostgreSQL database management
- Employs [Alembic](https://alembic.sqlalchemy.org/) for database migrations
- Ensures type safety with Pydantic for request and response models
- Enumerators or Enums are designed to be dynamically changable for scalability and flexibility

### User Authentication and Permissions Management
- Implements simple OAuth2 Authentication using FastAPI
- Implements permission checking based on Role and Permission using FastAPI dependency injection 

## API Endpoints

### User: `/users`
- Supports user CRUD operations and permission checks

### Movie: `/movie`
- Supports movie CRUD operations
- Movie data sourced from the [Movies TV Shows Database API](https://rapidapi.com/amrelrafie/api/movies-tv-shows-database)

### Series: `/series`
- Supports series CRUD operations
- Series data sourced from the [Movies TV Shows Database API](https://rapidapi.com/amrelrafie/api/movies-tv-shows-database)

### Anime: `/anime`
- Supports anime CRUD operations
- Anime data sourced from the [MyAnimeList API](https://rapidapi.com/felixeschmittfes/api/myanimelist)

## Additional References
- For more information on FastAPI, visit [FastAPI documentation](https://fastapi.tiangolo.com/)

## Similar Technologies
- Database migration alternatives: Entity Framework Core (EF Core) in .NET applications, Django migration files in Django
"""

app = FastAPI(
    title='Media ERM FastAPI (MEF)',
    description=description,
    summary='Testing FastAPI for backend RESTfull application.',
    version="1.0",
    contact={
        "name": "Fazreilie Bin Alep",
        "url": "https://www.linkedin.com/in/fazreilie-alep1",
        "email": "fazreilie122@gmail.com",
    })

@app.get("/")
async def root():
    return {"message": "Hello World"}

def fake_hash_password(password: str): # later change to used advanced hashing method
    return "fakehashed" + password

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = get_user_login(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me", summary="Get current User")
async def read_users_me(
    current_user: Annotated[CurrentUser, Depends(get_current_active_user)],
):
    return current_user

app.include_router(users.router)
app.include_router(anime.router)
app.include_router(movies.router)
app.include_router(series.router)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)