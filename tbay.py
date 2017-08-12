from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime

# Configuring Database (Engines, Bases & Sessions)
# create engine
engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
# create session
Session = sessionmaker(bind=engine)
session = Session()
# create declarative 
Base = declarative_base()


# The Item model
class Item(Base):
	__tablename__ = "items"
	
	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	description = Column(String)
	start_time = Column(DateTime, default=datetime.utcnow)
	
	
# The User model
class User(Base):
	__tablename__ = "users"
	
	id = Column(Integer, primary_key=True)
	username = Column(String, nullable=False)
	password = Column(String, nullable=False)
	
	
# The Bid model
class Bid(Base):
	__tablename__ = "bids"
	
	id = Column(Integer, primary_key=True)
	price = Column(Float, nullable=False)
	

# create the tables, issued by the declarative base (i.e. create table)
Base.metadata.create_all(engine)