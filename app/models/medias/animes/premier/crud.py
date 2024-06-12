from sqlalchemy.orm import Session

from .schema import PremierCreate
from .premier import Premier

def get_or_create_premier(db: Session, premier_data: PremierCreate) -> Premier:
    premier = db.query(Premier).filter(Premier.name == premier_data.name.lower()).first()
    if not premier:
        premier = Premier(name=premier_data.name.lower(), url=str(premier_data.url))
        db.add(premier)
        db.commit()
        db.refresh(premier)
    return premier