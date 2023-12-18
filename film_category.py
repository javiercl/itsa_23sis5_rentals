from flask import render_template, request, redirect, url_for, g, current_app
from flask_paginate import Pagination, get_page_parameter
import psycopg2
import logging

def index(page):

	with current_app.app_context():
		db = current_app.db
		user = current_app.user
		passw = current_app.passw
		server = current_app.server
  
	logging.basicConfig(level=logging.DEBUG)
	
	
   	# Connect to the database 
	conn = psycopg2.connect(database=db, user=user, password=passw, host=server, port="5432") 

	cur = conn.cursor() 
	cur.execute(f"SELECT count(*) from film_category") 
	datax = cur.fetchall()
	data2 = datax[0][0] # numero de registros encontrados en la tabla
 
	page = request.args.get(get_page_parameter(), type=int, default=int(page))
	if(page == 1):
		cur = conn.cursor() 
		cur.execute(f"SELECT fc.film_id, fc.category_id, fc.last_update, c.name, f.title FROM category c, film f, film_category fc WHERE c.category_id=fc.category_id and f.film_id=fc.film_id order by c.name, f.title limit {20} offset {0}") 
		datax = cur.fetchall()
	else:
		cur = conn.cursor() 
		cur.execute(f"SELECT fc.film_id, fc.category_id, fc.last_update, c.name, f.title FROM category c, film f, film_category fc WHERE c.category_id=fc.category_id and f.film_id=fc.film_id order by c.name, f.title LIMIT {20} offset { 20 * int(page)}") 
		datax = cur.fetchall()
     

	pagination = Pagination(page=page, data=datax, total=data2, css_framework='bootstrap4', record_name='film_category')

	# Select all products from the table 
	cur.execute('''SELECT film_id, title FROM film order by title''') 
	# Fetch the data 
	pelis = cur.fetchall() 

	# Select all products from the table 
	cur.execute('''SELECT category_id, name FROM category order by name''') 
	# Fetch the data 
	categs = cur.fetchall() 

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return render_template('film_category_view.html', data=datax, pagination=pagination, pelis=pelis, categs=categs) 


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
	category_id = request.form['category_id'] 

	# Insert the data into the table 
	cur.execute(f"INSERT INTO film_category (film_id,category_id) VALUES ({film_id},{category_id})") 

	# commit the changes 
	conn.commit() 

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return redirect(url_for('film_category')) 


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
	film_id = request.form['film_id'] 
	category_id = request.form['category_id'] 

	# Update the data in the table 
	cur.execute(f"UPDATE film_category SET film_id={film_id},category_id={category_id} WHERE film_id={film_id} and category_id={category_id}")

	# commit the changes 
	conn.commit() 
	cur.close() 
	conn.close() 
	return redirect(url_for('film_category')) 


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
	film_id = request.form['film_id'] 
	category_id = request.form['category_id'] 

	# Delete the data from the table 
	cur.execute(f"DELETE FROM film_category WHERE film_id={film_id} and category_id={category_id}") 

	# commit the changes 
	conn.commit() 

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return redirect(url_for('film_category')) 
