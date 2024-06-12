from datetime import date
from token import NUMBER
from typing import Optional, List
from pydantic import BaseModel, HttpUrl, Field


# carefull with language/languages inconsistency spelling, due to data received from api
class MovieBase(BaseModel):
    title: str 
    tagline: Optional[str] = None
    year: Optional[int] = None


class MovieCreate(MovieBase):
    id: Optional[int] = None
    imdb_id: str
    description: Optional[str] = None
    release_date: Optional[date] = None
    imdb_rating: Optional[float] = None
    vote_count: Optional[int] = None
    popularity: Optional[float] = None
    youtube_trailer_key: Optional[str] = None
    runtime: Optional[int] = None
    rated: Optional[str] = None
    genres: Optional[List[str]] = Field(default_factory=list)
    stars: Optional[List[str]] = Field(default_factory=list)
    directors: Optional[List[str]] = Field(default_factory=list)
    countries: Optional[List[str]] = Field(default_factory=list)
    language: Optional[List[str]] = Field(default_factory=list)
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Oppenheimer",
                    "description": "The story of J. Robert Oppenheimer's role in the development of the atomic bomb during World War II.",
                    "tagline": "The world forever changes.",
                    "year": "2023",
                    "release_date": "2023-07-19",
                    "imdb_id": "tt15398776",
                    "imdb_rating": "8.102",
                    "vote_count": "8078",
                    "popularity": "571.991",
                    "youtube_trailer_key": "bK6ldnjE3Y0",
                    "rated": "R",
                    "runtime": 181,
                    "genres": [
                        "Drama",
                        "History",
                        "Action",
                        "Biography",
                        "War"
                    ],
                    "stars": [
                        "Cillian Murphy",
                        "Emily Blunt",
                        "Matt Damon",
                        "Robert Downey Jr.",
                        "Florence Pugh",
                        "Josh Hartnett",
                        "Casey Affleck",
                        "Rami Malek",
                        "Kenneth Branagh",
                        "Benny Safdie",
                        "Jason Clarke",
                        "Dylan Arnold",
                        "Tom Conti",
                        "James D'Arcy",
                        "David Dastmalchian",
                        "Dane DeHaan",
                        "Alden Ehrenreich",
                        "Tony Goldwyn",
                        "Jefferson Hall",
                        "David Krumholtz",
                        "Matthew Modine",
                        "Scott Grimes",
                        "Kurt Koehler",
                        "John Gowans",
                        "Macon Blair",
                        "Harry Groener",
                        "Gregory Jbara",
                        "Ted King",
                        "Tim DeKay",
                        "Steven Houska",
                        "Petrie Willink",
                        "Matthias Schweigh\u00f6fer",
                        "Alex Wolff",
                        "Josh Zuckerman",
                        "Rory Keane",
                        "Michael Angarano",
                        "Emma Dumont",
                        "Sadie Stratton",
                        "Britt Kyle",
                        "Guy Burnet",
                        "Tom Jenkins",
                        "Louise Lombard",
                        "Michael Andrew Baker",
                        "Jeff Hephner",
                        "Olli Haaskivi",
                        "David Rysdahl",
                        "Josh Peck",
                        "Jack Quaid",
                        "Brett DelBuono",
                        "Gustaf Skarsg\u00e5rd",
                        "James Urbaniak",
                        "Trond Fausa Aurv\u00e5g",
                        "Devon Bostick",
                        "Danny Deferrari",
                        "Christopher Denham",
                        "Jessica Erin Martin",
                        "Ronald Auguste",
                        "M\u00e1t\u00e9 Haumann",
                        "Olivia Thirlby",
                        "Jack Cutmore-Scott",
                        "Harrison Gilbertson",
                        "James Remar",
                        "Will Roberts",
                        "Pat Skipper",
                        "Steve Coulter",
                        "Jeremy John Wells",
                        "Sean Avery",
                        "Adam Kroeger",
                        "Drew Kenney",
                        "Bryce Johnson",
                        "Flora Nolan",
                        "Kerry Westcott",
                        "Christina Hogue",
                        "Clay Bunker",
                        "Tyler Beardsley",
                        "Maria Teresa Zuppetta",
                        "Kate French",
                        "Gary Oldman",
                        "Hap Lawrence",
                        "Meg Schimelpfenig",
                        "Samarth Kaimliya",
                        "Andrew Bursiaga",
                        "Troy Bronson",
                        "Matt Snead",
                        "Jyoti",
                        "Emily Willis",
                        "Joe Russo",
                        "Colin Seifert",
                        "Yaser Al-Nyrabeah"
                    ],
                    "directors": [
                        "Richard Molloy",
                        "Steve Gehrke",
                        "Christopher Nolan",
                        "Nilo Otero",
                        "Andrew Stahl",
                        "Dixon McPhillips",
                        "Jesse Carmona"
                    ],
                    "countries": [
                        "United Kingdom",
                        "United States of America"
                    ],
                    "language": [
                        "Nederlands",
                        "English",
                        "en",
                        "Deutsch"
                    ],
                    "status": "OK",
                    "status_message": "Query was successful"
                }
            ]
        }
    }
    
class MovieUpdate(BaseModel):
    id: int
    title: Optional[str] = None 
    tagline: Optional[str] = None
    year: Optional[int] = None
    imdb_id: Optional[str] = None
    description: Optional[str] = None
    release_date: Optional[date] = None
    imdb_rating: Optional[float] = None
    vote_count: Optional[int] = None
    popularity: Optional[float] = None
    youtube_trailer_key: Optional[str] = None
    runtime: Optional[int] = None
    rated: Optional[str] = None
    genres: Optional[List[str]] = Field(default_factory=list)
    stars: Optional[List[str]] = Field(default_factory=list)
    directors: Optional[List[str]] = Field(default_factory=list)
    countries: Optional[List[str]] = Field(default_factory=list)
    languages: Optional[List[str]] = Field(default_factory=list)
    

class Movie(MovieBase):
    id: int

    class Config:
        orm_mode = True
        
        
class MovieListResponse(BaseModel):
    id: int
    imdb_id: str
    title: str
    year: int
    youtube_trailer_key: str