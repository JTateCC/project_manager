import os
import datetime
import math

from sqlalchemy import create_engine


def create_db_engine():
    db_path = os.path.join(os.getcwd(), 'db', 'project_manager.db')
    engine_path = 'sqlite:///' + db_path
    engine = create_engine(engine_path, echo=True)
    return engine

def date_to_int_conversion(date):
    return ((10000*date.year)+(100*date.day)+(date.month))

def int_to_date_conversion(dateint):
    print(dateint)
    year = math.floor(dateint/10000)
    day = math.floor((dateint - (year*10000))/100)
    month = dateint - year*10000 - day*100
    print(year, day, month)
    return(datetime.datetime(year, month, day))
