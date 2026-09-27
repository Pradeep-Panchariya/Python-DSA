from sqlalchemy import inspect

from app.database import engine
from app.init_db import initialize_database

def test_initialize_database_creates_incidents_table():
    initialize_database()

    inspector = inspect(engine)
    table_names = inspector.get_table_names()

    assert "incidents" in table_names