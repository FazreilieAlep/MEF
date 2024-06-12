from sqlalchemy.orm import Session

from . import schema
from .producer import Producer

def get_or_create_producer(db: Session, producer_data: schema.ProducerCreate) -> Producer:
    producer = db.query(Producer).filter(
        Producer.name == producer_data.name.lower()
    ).first()
    if not producer:
        producer = Producer(name=producer_data.name.lower(), url=str(producer_data.url))
        db.add(producer)
        db.commit()
        db.refresh(producer)
    return producer

def update_anime_producer(db: Session, producer_data: schema.Producer) -> Producer:
    producer = db.query(Producer).filter(Producer.id == producer_data.id).first()
    if not producer:
        producer = Producer(**producer_data.dict())
    return producer