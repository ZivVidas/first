from database import Base
from sqlalchemy import Column, ForeignKey,Integer,String,Boolean


class task(Base):
    __tablename__ = 'task'
    
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    Description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    CreatedBy = Column(Integer, ForeignKey("users.id"))
    
    