from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
import restaurant_dao

app = Flask(__name__)

@app.route('/restaurants/JSON/')
def restaurants():
  restaurants = restaurant_dao.getRestaurants()
  return jsonify(MenuItems=[i.serialize for i in restaurants])


@app.route('/restaurant/<int:restaurant_id>/menu-item/JSON/')
def restaurantMenuJSON(restaurant_id):
  items = restaurant_dao.getMenuItemsByRestaurant(restaurant_id)
  return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurant/<int:restaurant_id>/menu-item/<int:menu_id>/JSON/')
def restaurantMenuItemJSON(restaurant_id, menu_id):
  item = restaurant_dao.getMenuItemByRestaurant(restaurant_id, menu_id)
  return jsonify(MenuItem=item.serialize)


@app.route('/')
@app.route('/restaurants/')
def restaurantMenus():
  restaurants = restaurant_dao.getRestaurants()
  restaurants_arr = []

  for restaurant in restaurants:
  	items = restaurant_dao.getMenuItemsByRestaurant(restaurant.id)
  	setattr(restaurant, "items", items)
  	restaurants_arr.append(restaurant)


  return render_template('restaurants.html', restaurants=restaurants_arr)


@app.route('/restaurant/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
  restaurant = restaurant_dao.getRestaurant(restaurant_id)
  items = restaurant_dao.getMenuItemsByRestaurant(restaurant_id)

  return render_template('restaurant.html', restaurant=restaurant, items=items)


@app.route('/restaurant/<int:restaurant_id>/menu-item/<int:menu_id>/')
def restaurantMenuItem(restaurant_id, menu_id):
  restaurant = restaurant_dao.getRestaurant(restaurant_id)
  item = restaurant_dao.getMenuItemByRestaurant(restaurant_id, menu_id)

  return render_template('menu-item.html', restaurant=restaurant, item=item)


@app.route('/restaurant/new/', methods=['GET','POST'])
def newRestaurant():
  if request.method == 'POST':
    restaurant_dao.addRestaurant(request.form['name'])
    flash("New restaurant created!")
    return redirect(url_for('restaurantMenus'))
  else:
    return render_template('new-restaurant.html')


@app.route('/restaurant/<int:restaurant_id>/menu-item/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
  restaurant = restaurant_dao.getRestaurant(restaurant_id)
  if request.method == 'POST':
    restaurant_dao.addMenuItem(restaurant_id, request.form['name'], request.form['course'], request.form['price'], request.form['description'])
    flash("New menu item created!")
    return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
  else:
    return render_template('new-menu-item.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET','POST'])
def editRestaurant(restaurant_id):
  if request.method == 'POST':
    restaurant_dao.updateRestaurant(restaurant_id, request.form['name'])
    flash("Edited restaurant!")
    return redirect(url_for('restaurantMenus'))
  else:
    restaurant = restaurant_dao.getRestaurant(restaurant_id)
    return render_template('edit-restaurant.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu-item/<int:menu_id>/edit/', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
  if request.method == 'POST':
    restaurant_dao.updateMenuItem(menu_id, request.form['name'], request.form['course'], request.form['price'], request.form['description'])
    flash("Edited menu item!")
    return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
  else:
    restaurant = restaurant_dao.getRestaurant(restaurant_id)
    item = restaurant_dao.getMenuItemByRestaurant(restaurant_id, menu_id)
    return render_template('edit-menu-item.html', restaurant=restaurant, item=item)


@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET','POST']) 
def deleteRestaurant(restaurant_id):
  if request.method == 'POST':
    restaurant_dao.deleteRestaurant(restaurant_id)
    flash("Restaurant deleted!")
    return redirect(url_for('restaurantMenus'))
  else:
    restaurant = restaurant_dao.getRestaurant(restaurant_id)
    return render_template('delete-restaurant.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu-item/<int:menu_id>/delete/', methods=['GET','POST']) 
def deleteMenuItem(restaurant_id, menu_id):
  if request.method == 'POST':
    restaurant_dao.deleteMenuItem(menu_id)
    flash("Menu item deleted!")
    return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
  else:
    restaurant = restaurant_dao.getRestaurant(restaurant_id)
    item = restaurant_dao.getMenuItemByRestaurant(restaurant_id, menu_id)
    return render_template('delete-menu-item.html', restaurant=restaurant, item=item)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)