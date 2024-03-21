from database import Base

from sqlalchemy import Column,Integer,String,Boolean

class users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer,primary_key=True,index=True)
    email = Column(String)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    phonenumber = Column(String)


