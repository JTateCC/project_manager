import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def create_db_engine():
    db_path = os.path.join(os.getcwd(), 'db', 'project_manager.db')
    engine_path = 'sqlite:///' + db_path
    engine = create_engine(engine_path, echo=True)
    return engine

def date_to_int_conversion(date):
    return ((10000*date.year)+(100*date.day)+(date.month))

def int_to_date_conversion(dateint):
    # need to build
    pass