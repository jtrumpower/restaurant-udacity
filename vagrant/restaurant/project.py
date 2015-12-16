from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
import restaurant_dao

app = Flask(__name__)

@app.route('/')
@app.route('/restaurants/')
def restaurantMenus():
  restaurants = restaurant_dao.getRestaurants()
  output = ''
  for restaurant in restaurants:
    items = restaurant_dao.getMenuItemsByRestaurant(restaurant.id)
    output += '<a href="/restaurant/%s/">Restaurant <i>%s</i></a>' % (restaurant.id, restaurant.name)
    output += '</br>'
    output += '<a href="/restaurant/%s/menu-item/new">Create new Menu item for <i>%s</i></a>' % (restaurant.id, restaurant.name)
    output += '</br>'
    output += '</br>'
    for item in items:
      output += item.name
      output += '</br>'
      output += item.price
      output += '</br>'
      output += item.description
      output += '</br>'
      output += '<a href="/restaurant/%s/menu-item/%s/edit">Edit</a>' % (restaurant.id, item.id)
      output += '</br>'
      output += '<a href="/restaurant/%s/menu-item/%s/delete">Delete</a>' % (restaurant.id, item.id)
      output += '</br>'
      output += '</br>'
  return output


@app.route('/restaurant/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
  restaurant = restaurant_dao.getRestaurant(restaurant_id)
  items = restaurant_dao.getMenuItemsByRestaurant(restaurant_id)
  output = ''
  output = '<a href="/restaurant/%s/menu-item/new">Create new Menu item for <i>%s</i></a>' % (restaurant.id, restaurant.name)
  output += '</br>'
  output += '</br>'
  for i in items:
    output += i.name
    output += '</br>'
    output += i.price
    output += '</br>'
    output += i.description
    output += '</br>'
    output += '<a href="/restaurant/%s/menu-item/%s/edit">Edit</a>' % (restaurant.id, i.id)
    output += '</br>'
    output += '<a href="/restaurant/%s/menu-item/%s/delete">Delete</a>' % (restaurant.id, i.id)
    output += '</br>'
    output += '</br>'
  return output


# Task 1: Create route for newMenuItem function here

@app.route('/restaurant/<int:restaurant_id>/menu-item/new/')
def newMenuItem(restaurant_id):
  restaurant = restaurant_dao.getRestaurant(restaurant_id)
  output = ''
  output += '<h3>Create new menu item for <i>%s</i></h3>' % restaurant.name
  output += '<br />'
  output += '<form method="POST" action="/restaurant/%s/menu-item/new" >' % restaurant_id
  output += '<input type="text" name="name" placeholder="Item name" />'
  output += '<br />'
  output += '<input type="text" name="price" placeholder="Item price" />'
  output += '<br />'
  output += '<input type="text" name="description" placeholder="Item description" />'
  output += '</form>'
  return output

# Task 2: Create route for editMenuItem function here

@app.route('/restaurant/<int:restaurant_id>/menu-item/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
  restaurant = restaurant_dao.getRestaurant(restaurant_id)
  item = restaurant_dao.getMenuItemByRestaurant(restaurant_id, menu_id)
  output = ''
  output += '<h3>Edit menu item <i>%s</i> from restaurant <i>%s</i></h3>' % (item.name, restaurant.name)
  output += '<br />'
  output += '<form method="POST" action="/restaurant/%s/menu-item/%s/edit" >' % (restaurant_id, menu_id)
  output += '<input type="text" name="name" placeholder="Item name" value="%s" />' % item.name
  output += '<br />'
  output += '<input type="text" name="price" placeholder="Item price" value="%s" />' % item.price
  output += '<br />'
  output += '<input type="text" name="description" placeholder="Item description" value="%s" />' % item.description
  output += '</form>'
  return output

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurant/<int:restaurant_id>/menu-item/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
  restaurant = restaurant_dao.getRestaurant(restaurant_id)
  item = restaurant_dao.getMenuItemByRestaurant(restaurant_id, menu_id)

  delete_link = "/restaurant/%s/menu-item/%s/delete" % (restaurant_id, menu_id)

  output = ''
  output += '<h3>Delete menu item <i>%s</i> from restaurant <i>%s</i>?</h3>' % (item.name, restaurant.name)
  output += '<br />'
  output += '<form method="POST" action="/restaurant/%s/menu-item/%s/delete" >' % (restaurant_id, menu_id)
  output += '<a href="/restaurants/%s/"><input type="button" value="No" /></a>' % restaurant.id
  output += '<input type="submit" value="Yes" />'
  output += '</form>'
  return output

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)