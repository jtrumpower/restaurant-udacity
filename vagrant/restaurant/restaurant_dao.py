from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

def addRestaurant(name):
	restaurant = Restaurant(name = name)
	session.add(restaurant)
	session.commit()


def addMenuItem(restaurant_id, name, course, price, desc):
	menu_item = MenuItem(name = name, course = course, price = price, description = desc, restaurant_id = restaurant_id)
	session.add(menu_item)
	session.commit()


def getRestaurants():
	restaurants = session.query(Restaurant).all()

	return restaurants


def getMenuItemsByRestaurant(restaurant_id):
	menuItems = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()

	return menuItems


def getRestaurant(id):
	restaurant = session.query(Restaurant).filter_by(id = id).one()

	return restaurant


def getMenuItemByRestaurant(restaurant_id, menuItem_id):
	menuItem = session.query(MenuItem).filter_by(id = menuItem_id, restaurant_id=restaurant_id).one()

	return menuItem


def updateRestaurant(id, new_name):
	restaurant = session.query(Restaurant).filter_by(id = id).one()
	restaurant.name = new_name
	session.add(restaurant)
	session.commit()
	

def updateMenuItem(id, new_name, new_course, new_price, new_desc):
	menu_item = session.query(MenuItem).filter_by(id = id).one()
	if new_name != None and new_name != '':
		menu_item.name = new_name

	if new_course != None and new_course != '':
		menu_item.course = new_course

	if new_price != None and new_price != '':
		menu_item.price = new_price

	if new_desc != None and new_desc != '':
		menu_item.description = new_desc

	session.add(menu_item)
	session.commit()



def deleteRestaurant(id):
	restaurant = session.query(Restaurant).filter_by(id = id).one()
	session.delete(restaurant)
	session.commit()
	

def deleteMenuItem(id):
	menu_item = session.query(MenuItem).filter_by(id = id).one()
	session.delete(menu_item)
	session.commit()
	


