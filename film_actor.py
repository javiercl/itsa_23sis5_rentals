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
	mostrar = f"""SELECT fa.actor_id, fa.film_id, f.title AS film_title, fa.last_update
            FROM public.film_actor fa
            JOIN public.film f ON fa.film_id = f.film_id
            LIMIT 3;
        """
	cur.execute(mostrar) 

	# Fetch the data 
	datax = cur.fetchall() 

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return render_template('film_actor_view.html', data=datax) 


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
	a_id = request.form['aid']
	f_id = request.form['fid']

	# Insert the data into the table 
	cur.execute(f"INSERT INTO public.film_actor (actor_id, film_id, last_update) VALUES ({a_id}, {f_id}, CURRENT_TIMESTAMP);") 

	# commit the changes 
	conn.commit() 

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return redirect(url_for('film_actor')) 


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
	a_id = request.form['Actor_id'] 
	f_id = request.form['Film_id']
	id = request.form['actor_id']

	# Update the data in the table 
	update = f"""UPDATE public.film_actor
			SET actor_id = {a_id}, film_id = {f_id}
			WHERE actor_id = {id};
				"""
	cur.execute(update)

	# commit the changes 
	conn.commit()
	
	# close the cursor and connection 
	cur.close() 
	conn.close() 
	return redirect(url_for('Film_actor')) 


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
	a_id = request.form['actor_id'] 
	f_id = request.form['film_if']

	# Delete the data from the table 
	cur.execute(f"DELETE FROM public.film_actor WHERE actor_id = {a_id} AND film_id = {f_id}") 

	# commit the changes 
	conn.commit() 

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return redirect(url_for('film_actor')) 
