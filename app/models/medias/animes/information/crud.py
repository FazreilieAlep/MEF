from sqlalchemy.orm import Session

from app.models.medias.animes.anime.anime import Anime
from app.models.medias.animes.anime.schema import AnimeUpdate

from .schema import InformationCreate, InformationUpdate
from .information import Information
from ...enums.crud import get_or_create_enum
from ...host import Host
from ...enums_type import EnumsType


def create_anime_information(db: Session, information_data: InformationCreate, anime_id: int)-> Information:
    information = db.query(Information).filter(Information.anime_id == anime_id).first()
    if not information:
        status = get_or_create_enum(db, information_data.status, Host.MYANIMELIST, EnumsType.STATUS) if information_data.status else None
        aired = information_data.aired.lower() if information_data.aired else None
        broadcast = information_data.broadcast.lower() if information_data.broadcast else None
        information = Information(
            episode = information_data.episode,
            aired = aired,
            broadcast = broadcast,
            anime_id = anime_id,
            status_id = status.id
            )
        
        information.status = status
        
        db.add(information)
        db.commit()
        db.refresh(information)
    return information

def update_anime_information(db: Session, information_data: InformationUpdate, anime: Anime) -> Information:
    information = db.query(Information).filter(Information.anime_id == anime.id).first()
    
    if not information:
        information = Information(anime_id=anime.id)

    if information_data.status:
        status = get_or_create_enum(db, information_data.status, Host.MYANIMELIST, EnumsType.STATUS)
        information.status = status
    
    if information_data.aired:
        information.aired = information_data.aired.lower()
    
    if information_data.broadcast:
        information.broadcast = information_data.broadcast.lower()

    information.episode = information_data.episode
    
    db.add(information)
    db.commit()
    db.refresh(information)
    
    return information