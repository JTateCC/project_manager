

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


# Define The Table Classes
Base = declarative_base()


class Project(Base):
    __tablename__ = "Projects"
    ProjectID = Column(Integer, primary_key=True)
    Title = Column(String)
    Description = Column(String)
    Status = Column(Integer)
    Deadline = Column(Integer)
    Priority = Column(Integer)
    Tasks = relationship("Task", backref=backref("Projects"))


class Task(Base):
    __tablename__ = "Tasks"
    TaskID = Column(Integer, primary_key=True)
    Description = Column(String)
    Deadline = Column(Integer)
    CompletionDate = Column(Integer)
    Priority = Column(Integer)
    ProjectID = Column(Integer, ForeignKey(Project.ProjectID))

