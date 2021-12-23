

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


# Define The Table Classes
Base = declarative_base()


class Project(Base):
    __tablename__ = "Projects"
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True,  unique=True)
    Title = Column(String)
    Description = Column(String)
    Status = Column(Integer)
    CompletionDate = Column(Integer)
    Deadline = Column(Integer)
    Priority = Column(Integer)
    Tasks = relationship("Task", backref=backref("Projects"))


class Task(Base):
    __tablename__ = "Tasks"
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True, unique=True)
    Description = Column(String)
    Deadline = Column(Integer)
    Status = Column(Integer)
    CompletionDate = Column(Integer)
    projectid = Column(Integer, ForeignKey(Project.id, ondelete="CASCADE"))

