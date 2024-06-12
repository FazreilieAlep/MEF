from pydantic import BaseModel, HttpUrl


class AnimeBase(BaseModel):
    title_ov: str 
    title_en: str
    synopsis: str
    picture_url: HttpUrl


class AnimeCreate(AnimeBase):
    pass


class Anime(AnimeBase):
    id: int

    class Config:
        orm_mode = True
