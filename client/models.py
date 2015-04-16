from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Data(Base):
    
    __tablename__ = "db_data"

    id = Column(Integer, primary_key = True)
    phone_number = Column(Integer)
    message_type = Column(Integer)
    data = Column(String(255))
    status = Column(Integer)  
