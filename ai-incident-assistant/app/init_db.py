from app.database import Base, engine
from app.models import IncidentRecord

def initialize_database() -> None:
    Base.metadata.create_all(bind=engine)