from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

def addRestaurant(name):
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
	try: 
		restaurants = session.query(Restaurant).all()
	except:
		session.rollback()
		raise
	finally:
		session.close()

	return restaurants

def getMenuItemsByRestaurant(restaurant_id):
	try: 
		menuItems = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
	except:
		session.rollback()
		raise
	finally:
		session.close()

	return menuItems

def getRestaurant(id):
	try: 
		restaurant = session.query(Restaurant).filter_by(id = id).one()
	except:
		session.rollback()
		raise
	finally:
		session.close()

	return restaurant

def getMenuItemByRestaurant(restaurant_id, menuItem_id):
	try: 
		menuItem = session.query(MenuItem).filter_by(id = menuItem_id, restaurant_id=restaurant_id).one()
	except:
		session.rollback()
		raise
	finally:
		session.close()

	return menuItem

def updateRestaurant(id, newName):
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
	try:
		restaurant = session.query(Restaurant).filter_by(id = id).one()
		session.delete(restaurant)
		session.commit()
	except:
		session.rollback()
		raise
	finally:
		session.close()


