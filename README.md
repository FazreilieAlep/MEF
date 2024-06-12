# Media ERM FastAPI

Media ERM FastAPI (MEF API) is a robust API designed with [FastAPI](https://fastapi.tiangolo.com/) and [PostgreSQL](https://www.postgresql.org/) to efficiently manage media or content data such as movies, series, and anime details. It is specifically tailored to track the media content you have personally watched.

## Features

### Object Relational Mapping (ORM)
- **Database Management**: Utilizes [SQLAlchemy](https://www.sqlalchemy.org/) for PostgreSQL database management.
- **Database Migrations**: Employs [Alembic](https://alembic.sqlalchemy.org/) for seamless database migrations.
- **Type Safety**: Ensures type safety with Pydantic for request and response models.
- **Scalability and Flexibility**: Enumerators or Enums are designed to be dynamically changeable for scalability and flexibility.
- **Automatic Model Creation**: Simplifies the process by automatically creating object or model by adding a new SQLAlchemy model within the `/models` package.

### User Authentication and Permissions Management
- **Authentication**: Implements simple OAuth2 Authentication using FastAPI.
- **Permissions Management**: Implements permission checking based on Role and Permission using FastAPI dependency injection.

## API Endpoints

### User: `/users`
- Supports user CRUD operations and permission checks.

### Movie: `/movie`
- Supports CRUD operations for managing movies.
- Movie data is sourced from the [Movies TV Shows Database API](https://rapidapi.com/amrelrafie/api/movies-tv-shows-database).

### Series: `/series`
- Supports CRUD operations for managing TV series.
- Series data is sourced from the [Movies TV Shows Database API](https://rapidapi.com/amrelrafie/api/movies-tv-shows-database).

### Anime: `/anime`
- Supports CRUD operations for managing anime.
- Anime data is sourced from the [MyAnimeList API](https://rapidapi.com/felixeschmittfes/api/myanimelist).

## Additional References
- For more information on FastAPI, visit the [FastAPI documentation](https://fastapi.tiangolo.com/).

## Similar Technologies
- Database migration alternatives include Entity Framework Core (EF Core) in .NET applications and Django migration files in Django.

# Project Setup

1. **Create Virtual Environment**: Create a new Python virtual environment and activate it.
2. **Install Poetry**: Install Poetry by running `pip install poetry`.
3. **Install Dependencies**: Run `poetry install` **OR** `make install`.
4. **Database Migration**: Execute `cd app && alembic upgrade head` **OR** `make migrate` for initial database migration (ensure to update `DATABASE_URL` in `app/core/settings.py` with your database URL).
5. **Run Server**: Start the server by running `uvicorn app.main:app --reload` **OR** `make run-server`.

## Creating New Table in Database (SQLAlchemy Models)

The `app/models` folder or package is reserved to hold SQLAlchemy models. To add a new table:

1. **Organize Models**: Organize your SQLAlchemy models within the `app/models` folder.
2. **Special Files**: Ensure `crud.py`, `schema.py`, `associations.py`, and `__init__.py` are present. They serve specific functions for database and API operations.
3. **Exclude Special Files**: If there are any files you don't want Alembic migrations to detect as SQLAlchemy models, add their names to `recursive_import(app.models, exclude_files=['crud', 'schema', '__init__', 'associations', 'your_special_file'])` in `app/alembic/env.py`. For more detail on Alembic env.py file, refer [here](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)
4. **Migration**: To migrate newly created models, run `make migrations` followed by `make migrate` in the project command prompt.

`app/models` special file details:
- `crud.py` : store CRUD operations method for the model(s)
- `schema.py` : store Pydantic model classes that will be used for an API request body or response body. Using Pydantic is powerful as it automatically handle type checks and extra data validation as per user defined
- `association.py` : store association tables for many-to-many relationship tables
- `__init__` : python package declaration

