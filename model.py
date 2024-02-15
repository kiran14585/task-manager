from sqlalchemy import Column,Integer,String,Boolean,DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base =  declarative_base()

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String,index=True)
    description = Column(String)
    completed = Column(Boolean)
    created_at = Column(DateTime,default=datetime.now())
