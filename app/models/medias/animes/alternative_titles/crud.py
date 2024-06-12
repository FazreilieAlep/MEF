from sqlalchemy.orm import Session, synonym

from .schema import AlternativeTitlesCreate
from .alternative_titles import Alternative_Titles

def get_or_create_alt_title(db: Session, alt_titles_data: AlternativeTitlesCreate, anime_id: int) -> Alternative_Titles:
    alt_title = db.query(Alternative_Titles).filter(Alternative_Titles.anime_id == anime_id).first()
    if not alt_title:
        synonym_title = alt_titles_data.synonym.lower() if alt_titles_data.synonym else None
        alt_title = Alternative_Titles(
            anime_id=anime_id,
            synonym=synonym_title,
            japanese=alt_titles_data.japanese,
        )
        db.add(alt_title)
        db.commit()
        db.refresh(alt_title)
    return alt_title