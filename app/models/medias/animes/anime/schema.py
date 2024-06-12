from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional
from ..alternative_titles.schema import AlternativeTitlesCreate, AlternativeTitles, AlternativeTitlesUpdate
from ..information.schema import InformationCreate, Information, InformationUpdate
from ..producer.schema import ProducerCreate, Producer, ProducerCreateOrUpdate
from ..licensor.schema import LicensorCreate, Licensor, LicensorCreateOrUpdate
from ..studio.schema import StudioCreate, Studio, StudioCreateOrUpdate
from ...enums.schema import EnumsCreate, Enums, EnumsCreateOrUpdate
from ..premier.schema import PremierCreate, Premier, PremierCreateOrUpdate


class AnimeBase(BaseModel):
    title_ov: Optional[str] = None 
    title_en: Optional[str] = None
    synopsis: str
    picture_url: HttpUrl


class AnimeCreate(AnimeBase):
    id: Optional[int] = None
    myanimelist_id: Optional[int] = None
    alternative_titles: Optional[AlternativeTitlesCreate] = None
    information: Optional[InformationCreate] = None
    producers: Optional[List[ProducerCreate]] = Field(default_factory=list)
    licensors: Optional[List[LicensorCreate]] = Field(default_factory=list)
    studios: Optional[List[StudioCreate]] = Field(default_factory=list)
    genres: Optional[List[EnumsCreate]] = Field(default_factory=list)
    demographics: Optional[List[EnumsCreate]] = Field(default_factory=list)
    type: Optional[EnumsCreate] = None
    premiered: Optional[PremierCreate] = None
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title_ov": "Sousou no Frieren",
                    "title_en": "Frieren: Beyond Journey's End",
                    "synopsis": "During their decade-long quest to defeat the Demon King, the members of the hero's party\u2014Himmel himself, the priest Heiter, the dwarf warrior Eisen, and the elven mage Frieren\u2014forge bonds through adventures and battles, creating unforgettable precious memories for most of them.\n\r\nHowever, the time that Frieren spends with her comrades is equivalent to merely a fraction of her life, which has lasted over a thousand years. When the party disbands after their victory, Frieren casually returns to her \"usual\" routine of collecting spells across the continent. Due to her different sense of time, she seemingly holds no strong feelings toward the experiences she went through.\n\r\nAs the years pass, Frieren gradually realizes how her days in the hero's party truly impacted her. Witnessing the deaths of two of her former companions, Frieren begins to regret having taken their presence for granted; she vows to better understand humans and create real personal connections. Although the story of that once memorable journey has long ended, a new tale is about to begin.\n\r\n[Written by MAL Rewrite]",
                    "picture_url": "https://cdn.myanimelist.net/images/anime/1015/138006.jpg",
                    "alternative_titles": {
                        "synonym": "Frieren at the Funeral",
                        "japanese": "\u846c\u9001\u306e\u30d5\u30ea\u30fc\u30ec\u30f3"
                    },
                    "information": {
                        "aired": "Sep 29, 2023 to Mar 22, 2024",
                        "episode": 28,
                        "broadcast": "Fridays at 23:00 (JST)",
                        "status": {
                            "name": "Finished Airing"
                        }
                    },
                    "type": {
                        "name": "TV",
                        "url": "https://myanimelist.nethttps://myanimelist.net/topanime.php?type=tv"
                    },
                    "premiered": {
                        "name": "Fall 2023",
                        "url": "https://myanimelist.nethttps://myanimelist.net/anime/season/2023/fall"
                    },
                    "producers": [
                        {
                            "name": "Aniplex",
                            "url": "https://myanimelist.net/anime/producer/17/Aniplex"
                        },
                        {
                            "name": "Dentsu",
                            "url": "https://myanimelist.net/anime/producer/53/Dentsu"
                        },
                        {
                            "name": "Shogakukan-Shueisha Productions",
                            "url": "https://myanimelist.net/anime/producer/62/Shogakukan-Shueisha_Productions"
                        },
                        {
                            "name": "Nippon Television Network",
                            "url": "https://myanimelist.net/anime/producer/1003/Nippon_Television_Network"
                        },
                        {
                            "name": "TOHO animation",
                            "url": "https://myanimelist.net/anime/producer/1143/TOHO_animation"
                        },
                        {
                            "name": "Shogakukan",
                            "url": "https://myanimelist.net/anime/producer/1430/Shogakukan"
                        }
                    ],
                    "studios": [
                        {
                            "name": "Madhouse",
                            "url": "https://myanimelist.net/anime/producer/11/Madhouse"
                        }
                    ],
                    "genres": [
                        {
                            "name": "Adventure",
                            "url": "https://myanimelist.net/anime/genre/2/Adventure"
                        },
                        {
                            "name": "Drama",
                            "url": "https://myanimelist.net/anime/genre/8/Drama"
                        },
                        {
                            "name": "Fantasy",
                            "url": "https://myanimelist.net/anime/genre/10/Fantasy"
                        }
                    ],
                    "demographics": [
                        {
                            "name": "Shounen",
                            "url": "https://myanimelist.net/anime/genre/27/Shounen"
                        }
                    ]
                }
            ]
        }
    }


class Anime(AnimeBase):
    id: int

    class Config:
        orm_mode = True
        
class AnimeUpdate(BaseModel):
    id: Optional[int] = None
    myanimelist_id: Optional[int] = None
    title_ov: Optional[str] = None 
    title_en: Optional[str] = None 
    synopsis: Optional[str] = None 
    picture_url: Optional[HttpUrl] = None 
    alternative_titles: Optional[AlternativeTitlesUpdate] = None
    information: Optional[InformationUpdate] = None
    producers: Optional[List[ProducerCreateOrUpdate]] = None
    licensors: Optional[List[LicensorCreateOrUpdate]] = None
    studios: Optional[List[StudioCreateOrUpdate]] = None
    genres: Optional[List[EnumsCreateOrUpdate]] = None
    demographics: Optional[List[EnumsCreateOrUpdate]] = None
    type: Optional[EnumsCreateOrUpdate] = None
    premiered: Optional[PremierCreateOrUpdate] = None
    
class AnimeListResponse(BaseModel):
    id: int
    myanimelist_id: Optional[int]
    title_ov: str
    title_en: Optional[str]
    synopsis: Optional[str]
    picture_url: Optional[str]