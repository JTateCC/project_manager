import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def create_db_engine():
    db_path = os.path.join(os.getcwd(), 'db', 'project_manager.db')
    engine_path = 'sqlite:///' + db_path
    engine = create_engine(engine_path)
    return engine

def create_session():
    return sessionmaker(create_db_engine())

