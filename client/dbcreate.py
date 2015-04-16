# table_def.py
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
engine = create_engine('mysql://sohil4932:Hetvi_1234@mywhatsappdb.database.windows.net:1443/mywhatsappdb', echo=True)
Base = declarative_base()  
 
########################################################################
class Data(Base):
    
    __tablename__ = "db_data"

    id = Column(Integer, primary_key = True)
    phone_number = Column(Integer)
    message_type = Column(Integer)
    data = Column(String(255))
    status = Column(Integer)  
 
    #----------------------------------------------------------------------
    def __init__(self, phone_number, message_type, data, status):
        """"""
        self.phone_number = phone_number
        self.message_type = message_type
        self.data = data
        self.status = status
 
# create tables
Base.metadata.create_all(engine)