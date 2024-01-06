from flask import render_template, request, redirect, url_for, g, current_app
from flask_paginate import Pagination, get_page_parameter
import psycopg2
import logging

'''
TABLA DE INVENTARIO
EQUIPO #7
* MENDOZA ROSAS LUIS FRANCISCO
* TORRES CERVANTES LUIS ENRIQUE
* GASCA RAMIREZ ALFREDO
'''

def index(page2):

	with current_app.app_context():
		db = current_app.db
		user = current_app.user
		passw = current_app.passw
		server = current_app.server
  
	logging.basicConfig(level=logging.DEBUG)
	
	
   	# Connect to the database 
	conn = psycopg2.connect(database=db, user=user, password=passw, host=server, port="5432") 

	cur = conn.cursor() 
	cur.execute(f"SELECT count(*) from inventory") 
	datax = cur.fetchall()
	data2 = datax[0][0] # numero de registros encontrados en la tabla
 
	page2 = request.args.get(get_page_parameter(), type=int, default=int(page2))
	if(page2 == 1):
		cur = conn.cursor() 
		cur.execute(f"SELECT i.inventory_id, i.film_id, i.store_id, i.last_update, f.title FROM inventory i, film f WHERE f.film_id=i.film_id order by i.inventory_id limit {20} offset {0}") 
		datax = cur.fetchall()
	else:
		cur = conn.cursor() 
		cur.execute(f"SELECT i.inventory_id, i.film_id, i.store_id, i.last_update, f.title FROM inventory i, film f WHERE f.film_id=i.film_id order by i.inventory_id LIMIT {20} offset { 20 * int(page2)}") 
		datax = cur.fetchall()

	pagination = Pagination(page=page2, data=datax, total=data2, css_framework='bootstrap4', record_name='inventory')

	# Select all products from the table 
	cur.execute('''select film_id, title from film order by film_id''') 
	# Fetch the data 
	pelis = cur.fetchall()
 
    # Select all products from the table 
	cur.execute('''select store_id from inventory group by store_id''') 
	# Fetch the data 
	storeid = cur.fetchall()
	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return render_template('inventory_view.html', data=datax, pagination=pagination, pelis=pelis,store=storeid) 


def create():
    
	with current_app.app_context():
		db = current_app.db
		user = current_app.user
		passw = current_app.passw
		server = current_app.server
	
 	# Connect to the database 
	conn = psycopg2.connect(database=db, user=user, password=passw, host=server, port="5432") 

	cur = conn.cursor() 

	# Get the data from the form 
	film_id = request.form['film_id'] 
	store_id = request.form['store_id'] 

	# Insert the data into the table 
	cur.execute(f"INSERT INTO inventory (film_id,store_id) VALUES ({film_id},{store_id})") 

	# commit the changes 
	conn.commit() 

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return redirect(url_for('inventory')) 


def update():
    
	with current_app.app_context():
		db = current_app.db
		user = current_app.user
		passw = current_app.passw
		server = current_app.server
 
	# Connect to the database 
	conn = psycopg2.connect(database=db, user=user, password=passw, host=server, port="5432") 

	cur = conn.cursor() 

	# Get the data from the form 
	inventory_id = request.form['inventory_id'] 
	film_id = request.form['film_id'] 
	store_id = request.form['store_id'] 

	# Update the data in the table 
	cur.execute(f"UPDATE inventory SET film_id='{film_id}', store_id='{store_id}' WHERE inventory_id={inventory_id}")

	# commit the changes 
	conn.commit() 
	cur.close() 
	conn.close() 
	return redirect(url_for('inventory')) 


def delete():
    
	with current_app.app_context():
		db = current_app.db
		user = current_app.user
		passw = current_app.passw
		server = current_app.server
 
	# Connect to the database 
	conn = psycopg2.connect(database=db, user=user, password=passw, host=server, port="5432") 
	cur = conn.cursor() 

	# Get the data from the form 
	inventory_id = request.form['inventory_id'] 

	# Delete the data from the table 
	cur.execute(f"DELETE FROM inventory WHERE inventory_id={inventory_id}") 

	# commit the changes 
	conn.commit() 

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return redirect(url_for('inventory')) 
