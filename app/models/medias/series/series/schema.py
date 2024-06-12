from datetime import date
from token import NUMBER
from typing import Optional, List
from pydantic import BaseModel, HttpUrl, Field
from ...enums.schema import EnumsCreate, Enums, EnumsCreateOrUpdate


class SeriesBase(BaseModel):
    title: str 
    runtime: Optional[int] = None
    youtube_trailer_key: Optional[str] = None
    year_started: int
    


class SeriesCreate(SeriesBase):
    id: Optional[int] = None
    imdb_id: Optional[str] = None
    description: Optional[str] = None
    release_date: Optional[date] = None
    imdb_rating: Optional[float] = None
    vote_count: Optional[int] = None
    popularity: Optional[float] = None
    rated: Optional[str] = None
    genres: Optional[List[str]] = Field(default_factory=list)
    stars: Optional[List[str]] = Field(default_factory=list)
    creators: Optional[List[str]] = Field(default_factory=list)
    countries: Optional[List[str]] = Field(default_factory=list)
    language: Optional[List[str]] = Field(default_factory=list)
    production_companies: Optional[List[str]] = Field(default_factory=list)
    networks: Optional[List[str]] = Field(default_factory=list)
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Start-Up",
                    "description": "Young entrepreneurs aspiring to launch virtual dreams into reality compete for success and love in the cutthroat world of Korea's high-tech industry.",
                    "release_date": "2020-10-17",
                    "imdb_id": "tt12867810",
                    "imdb_rating": "8.3",
                    "vote_count": "287",
                    "popularity": "40.145",
                    "youtube_trailer_key": "",
                    "rated": "TV-14",
                    "runtime": 72,
                    "year_started": 2020,
                    "genres": [
                        "Drama",
                        "Comedy",
                        "Romance"
                    ],
                    "stars": [
                        "Bae Suzy",
                        "Nam Joo-hyuk",
                        "Kim Seon-ho",
                        "Kang Han-na",
                        "Kim Hae-sook",
                        "Kim Do-wan",
                        "Kim Won-hae",
                        "Song Sun-mi",
                        "Yoo Su-bin",
                        "Seo Yi-sook",
                        "Song Seon-mi",
                        "Nam Joo-Hyuk"
                    ],
                    "creators": [
                        "Park Hye-ryun"
                    ],
                    "countries": [
                        "KR",
                        "Kr"
                    ],
                    "language": [
                        "en",
                        "ko",
                        "th"
                    ],
                    "production_companies": [
                        "Studio Dragon",
                        "HighZium Studio",
                        "HiSTORY"
                    ],
                    "networks": [
                        "tvN",
                        "Netflix"
                    ],
                    "status": "OK",
                    "status_message": "Query was successful"
                }
            ]
        }
    }
    
class SeriesUpdate(BaseModel):
    id: int
    imdb_id: Optional[str] = None
    title: Optional[str] = None 
    runtime: Optional[int] = None
    youtube_trailer_key: Optional[str] = None
    year_started: Optional[int] = None
    description: Optional[str] = None
    release_date: Optional[date] = None
    imdb_rating: Optional[float] = None
    vote_count: Optional[int] = None
    popularity: Optional[float] = None
    rated: Optional[str] = None
    genres: Optional[List[str]] = Field(default_factory=list)
    stars: Optional[List[str]] = Field(default_factory=list)
    creators: Optional[List[str]] = Field(default_factory=list)
    countries: Optional[List[str]] = Field(default_factory=list)
    language: Optional[List[str]] = Field(default_factory=list)
    production_companies: Optional[List[str]] = Field(default_factory=list)
    networks: Optional[List[str]] = Field(default_factory=list)
    
    

class Series(SeriesBase):
    id: int

    class Config:
        orm_mode = True


class SeriesListResponse(BaseModel):
    id: int
    imdb_id: str
    title: str
    year_started: int
    youtube_trailer_key: str