from sqlalchemy.orm import Session

from .schema import StudioCreate
from .studio import Studio

def get_or_create_studio(db: Session, studio_data: StudioCreate) -> Studio:
    studio = db.query(Studio).filter(Studio.name == studio_data.name.lower()).first()
    if not studio:
        studio = Studio(name=studio_data.name.lower(), url=str(studio_data.url))
        db.add(studio)
        db.commit()
        db.refresh(studio)
    return studio