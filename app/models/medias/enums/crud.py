from sqlalchemy.orm import Session

from .schema import EnumsCreate
from .enums import Enums
from ...medias.host import Host
from ...medias.enums_type import EnumsType


def get_or_create_enum(db: Session, enums_data: EnumsCreate, site: Host, type: EnumsType) -> Enums:
    enums = db.query(Enums).filter(Enums.site == site, Enums.type == type, Enums.value == enums_data.name.lower()).first()
    if not enums:
        enums = Enums(site=site, type=type, value=enums_data.name.lower(), url=str(enums_data.url))
        db.add(enums)
        db.commit()
        db.refresh(enums)
    return enums