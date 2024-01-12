from flask import render_template, request, redirect, url_for, g, current_app
import psycopg2 


def index():
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
	cur.execute('''SELECT * FROM actor limit 5''') 

	# Fetch the data 
	datax = cur.fetchall() 

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return render_template('actor_view.html', data=datax) 


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
	apellido = request.form['apellido']

	# Insert the data into the table 
	cur.execute(f"INSERT INTO public.actor (first_name, last_name, last_update) VALUES ('{name}', '{apellido}', CURRENT_TIMESTAMP)") 

	# commit the changes 
	conn.commit() 

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return redirect(url_for('actor')) 


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
	apellido = request.form['apellido']
	id = request.form['actor_id']

	# Update the data in the table 
	cur.execute(f"UPDATE public.actor SET first_name = '{name}', last_name = '{apellido}', last_update = CURRENT_TIMESTAMP WHERE actor_id = {id};")

	# commit the changes 
	conn.commit()
	
	# close the cursor and connection 
	cur.close() 
	conn.close() 
	return redirect(url_for('actor')) 


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
	id = request.form['actor_id'] 

	# Delete the data from the table 
	delete = f"""
	DELETE FROM public.film_actor WHERE actor_id = {id};
	DELETE FROM actor WHERE actor_id={id};
			"""
	cur.execute(delete) 

	# commit the changes 
	conn.commit() 

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return redirect(url_for('actor')) 
