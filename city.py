from flask import render_template, request, redirect, url_for, g, current_app
from flask_paginate import Pagination, get_page_parameter
import psycopg2
import logging

#Adilene Estefania Comino Ibarra
#Tabla City
#Equipo6


def index(page4):

	with current_app.app_context():
		db = current_app.db
		user = current_app.user
		passw = current_app.passw
		server = current_app.server
  
	logging.basicConfig(level=logging.DEBUG)
	
	
   	# Connect to the database 
	conn = psycopg2.connect(database=db, user=user, password=passw, host=server, port="5432") 

	cur = conn.cursor() 
	cur.execute(f"SELECT count(*) from city")  
	datax = cur.fetchall()
	data3 = datax[0][0] # numero de registros encontrados en la tabla
 
	page4= request.args.get(get_page_parameter(), type=int, default=int(page4))
	if(page4 == 1):
		cur = conn.cursor() 
		cur.execute(f"SELECT c.city_id, c.city, co.country, c.last_update, c.country_id, co.country_id FROM city c, country co WHERE c.country_id = co.country_id order by c.city_id desc limit {20} offset {0}") 
		datax = cur.fetchall()
	else:
		cur = conn.cursor() 
		cur.execute(f"SELECT c.city_id, c.city, co.country, c.last_update, c.country_id, co.country_id FROM city c, country co WHERE c.country_id = co.country_id order by c.city_id desc limit {20} offset { 20 * int(page4)}") 
		datax = cur.fetchall()

	pagination = Pagination(page=page4, data=datax, total=data3, css_framework='bootstrap4', record_name='city')

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return render_template('city_view.html', data=datax, pagination=pagination) 


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
	name = request.form['name'] 
	
	# Insert the data into the table 
	cur.execute(f"INSERT INTO city (city, country_id) VALUES ('{name}',1)") 

	# commit the changes 
	conn.commit() 

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return redirect(url_for('city')) 


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
	name = request.form['city'] 
	id = request.form['city_id'] 
	id2 = request.form['country_id']

	# Update the data in the table 
	cur.execute(f"UPDATE city SET city='{name}', country_id='{id2}' WHERE city_id={id}")

	# commit the changes 
	conn.commit() 
	cur.close() 
	conn.close() 
	return redirect(url_for('city')) 


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
	id = request.form['city_id'] 

	# Delete the data from the table 
	cur.execute(f"DELETE FROM city WHERE city_id={id}") 
	
	# commit the changes 
	conn.commit() 

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return redirect(url_for('city'))