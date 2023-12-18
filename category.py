from flask import render_template, request, redirect, url_for, g, current_app
#import logging
import psycopg2 


def index():

	with current_app.app_context():
		db = current_app.db
		user = current_app.user
		passw = current_app.passw
		server = current_app.server

	#logging.basicConfig(level=logging.DEBUG)
	#current_app.logger.info(f"Base de datos {db}")
	
	# Connect to the database 
	conn = psycopg2.connect(database=db, user=user, password=passw, host=server, port="5432") 

	# create a cursor 
	cur = conn.cursor() 

	# Select all products from the table 
	cur.execute('''SELECT * FROM category''') 

	# Fetch the data 
	datax = cur.fetchall() 

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return render_template('category_view.html', data=datax) 


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
	cur.execute(f"INSERT INTO category (name) VALUES ('{name}')") 

	# commit the changes 
	conn.commit() 

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return redirect(url_for('category')) 


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
	name = request.form['name'] 
	id = request.form['category_id'] 

	# Update the data in the table 
	cur.execute(f"UPDATE category SET name='{name}' WHERE category_id={id}")

	# commit the changes 
	conn.commit() 
	cur.close() 
	conn.close() 
 
	return redirect(url_for('category')) 


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
	id = request.form['category_id'] 

	# Delete the data from the table 
	cur.execute(f"DELETE FROM category WHERE category_id={id}") 

	# commit the changes 
	conn.commit() 

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return redirect(url_for('category')) 
