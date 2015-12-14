from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

def getSession():
	engine = create_engine('sqlite:///restaurantmenu.db')
	Base.metadata.bind = engine
	DBSession = sessionmaker(bind = engine)
	session = DBSession()
	return session

def addRestaurant(name):
	session = getSession()
	try:
		restaurant = Restaurant(name = name)
		session.add(restaurant)
		session.commit()
	except:
		session.rollback()
		raise
	finally:
		session.close()

def getRestaurants():
	session = getSession()
	try: 
		restaurants = session.query(Restaurant).all()
	except:
		session.rollback()
		raise
	finally:
		session.close()

	return restaurants

def getRestaurant(id):
	session = getSession()
	try: 
		restaurant = session.query(Restaurant).filter_by(id = id).one()
	except:
		session.rollback()
		raise
	finally:
		session.close()

	return restaurant

def updateRestaurant(id, newName):
	session = getSession()
	try:
		restaurant = session.query(Restaurant).filter_by(id = id).one()
		restaurant.name = newName
		session.add(restaurant)
		session.commit()
	except:
		session.rollback()
		raise
	finally:
		session.close()

def deleteRestaurant(id):
	session = getSession()
	try:
		restaurant = session.query(Restaurant).filter_by(id = id).one()
		session.delete(restaurant)
		session.commit()
	except:
		session.rollback()
		raise
	finally:
		session.close()


