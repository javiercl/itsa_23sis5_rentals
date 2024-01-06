from flask import render_template, request, redirect, url_for, g, current_app
import psycopg2 

'''
	Equipo #2:
	Walter Jahir Ambriz Reyna
	Ana Laura Cortez Cortes
	Daniel Alejandro Gonzalez Rodriguez
'''

def index():
#Hola profe cisneros 
	with current_app.app_context():
		db = current_app.db
		user = current_app.user
		passw = current_app.passw
		server = current_app.server
	
   	# Connect to the database 
	conn = psycopg2.connect(database=db, user=user, password=passw, host=server, port="5432") 

	# create a cursor 
	cur = conn.cursor() 

	# Select all products from the table 
	cur.execute('''SELECT * FROM language''') 

	# Fetch the data 
	datax = cur.fetchall() 

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return render_template('language_view.html', data=datax) 


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
	cur.execute(f"INSERT INTO language (name) VALUES ('{name}')") 

	# commit the changes 
	conn.commit() 

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return redirect(url_for('language')) 


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
	cur.execute(f"UPDATE language SET name='{name}' WHERE lenguage_id={id}")

	# commit the changes 
	conn.commit()
	
	# close the cursor and connection 
	cur.close() 
	conn.close() 
	return redirect(url_for('language')) 


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
	cur.execute(f"DELETE FROM language WHERE language_id={id}") 

	# commit the changes 
	conn.commit() 

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return redirect(url_for('language')) 
