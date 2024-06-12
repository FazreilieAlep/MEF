from sqlalchemy.orm import Session

from .schema import LicensorCreate
from .licensor import Licensor

def get_or_create_licensor(db: Session, licensor_data: LicensorCreate) -> Licensor:
    licensor = db.query(Licensor).filter(Licensor.name == licensor_data.name.lower()).first()
    if not licensor:
        licensor = Licensor(name=licensor_data.name.lower(), url=str(licensor_data.url))
        db.add(licensor)
        db.commit()
        db.refresh(licensor)
    return licensor