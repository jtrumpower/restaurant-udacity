from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

def getSession():
	engine = create_engine('sqlite:///restaurtantmenu.db')
	Base.metadata.bind = engine
	DBSession = sessionmaker(bind = engine)
	session = DBSession()
	return session

def addRestaurant(name):
	session = getSession()
	restaurant = Restaurant(name = name)
	session.add(restaurant)
	session.commit()

def getRestaurants():
	session = getSession()
	restaurants = session.query(Restaurant).all()
	return restaurants

def getRestaurant(id):
	session = getSession()
	restaurant = session.query(Restaurant).filter_by(id = id)
	return restaurant

def updateRestaurant(id, newName):
	session = getSession()
	restaurant = session.query(Restaurant).filter_by(id = id)
	restaurant.name = newName
	session.add(restaurant)
	session.commit()

def deleteRestaurant(id):
	session = getSession()
	restaurant = session.query(Restaurant).filter_by(id = id)
	session.delete(restaurant)
	session.commit()