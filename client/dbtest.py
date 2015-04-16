from sqlalchemy import Column, Date, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Data

from config import config

engine = create_engine(config.SQLDATABASE_URI)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

count = session.query(Data).filter(Data.status==0).count()

print count