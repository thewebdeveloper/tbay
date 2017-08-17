from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship


# Configuring Database (Engines, Bases & Sessions)
# create engine
engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay_v2')
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
	
	owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
	
	bids = relationship("Bid", backref="item")
	
	
# The User model
class User(Base):
	__tablename__ = "users"
	
	id = Column(Integer, primary_key=True)
	username = Column(String, nullable=False)
	password = Column(String, nullable=False)
	
	items = relationship("Item", backref="owner")
	bids = relationship("Bid", backref="bidder")
	
	
# The Bid model
class Bid(Base):
	__tablename__ = "bids"
	
	id = Column(Integer, primary_key=True)
	price = Column(Float, nullable=False)
	
	bidder_id = Column(Integer, ForeignKey("users.id"), nullable=False)
	item_id = Column(Integer, ForeignKey("items.id"), nullable=False)


# create the tables, issued by the declarative base (i.e. create table)
Base.metadata.create_all(engine)


# Add three users to the database
abdullah = User(username="Abdullah Altamimi", password="abcd")
amira = User(username="Amira Alnaggar", password="abcd")
alia = User(username="Alia Altamimi", password="abcd")

session.add_all([abdullah, amira, alia])
session.commit()


# Make one user auction a baseball
baseball = Item(name="Baseball", description="American Baseball", owner_id=1)

session.add(baseball)
session.commit()

#Have each other user place two bids on the baseball
bid1 = Bid(price=5.00, bidder_id=2, item_id=1)
bid2 = Bid(price=6.50, bidder_id=3, item_id=1)
bid3 = Bid(price=7.00, bidder_id=2, item_id=1)
bid4 = Bid(price=7.50, bidder_id=3, item_id=1)

session.add_all([bid1, bid2, bid3, bid4])
session.commit()


# Perform a query to find out which user placed the highest bid
result = session.query(Bid.price, User.username).filter(Bid.bidder_id == User.id).order_by(Bid.price.desc()).all()
print("The Highest bidder is {} with price of ${}".format(result[0][1], result[0][0]))


