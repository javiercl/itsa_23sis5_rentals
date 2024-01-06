from flask import render_template, request, redirect, url_for, g, current_app
import psycopg2 

'''
EQUIPO #5
Lúa Ruiz Ulises 
Ceja Mendoza José Ángel 
Suarez Espinoza Cristian 
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
	ver= f'''SELECT c.customer_id,c.store_id,c.first_name,c.last_name,c.email,c.address_id,c.activebool,c.active, a.address,a.district,a.postal_code,a.phone
                FROM customer c
                JOIN address a ON c.address_id = a.address_id
		    '''
	cur.execute(ver) 

	# Fetch the data 
	datax = cur.fetchall() 

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return render_template('customer_view.html', data=datax) 


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
	store_id = request.form['store_id']
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	email = request.form['email']
	address_id = request.form['address_id']
	activebool = 't' if 'activebool' in request.form else 'f'
	
	crearC = f"""
            INSERT INTO customer (store_id, first_name, last_name, email, address_id, activebool, create_date)
            VALUES ({store_id}, '{first_name}', '{last_name}', '{email}', {address_id}, {activebool}, now());
        """

	# Insert the data into the table 
	cur.execute(crearC) 

	# commit the changes 
	conn.commit() 

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return redirect(url_for('customer')) 


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
	id = request.form['customer_id']
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	email = request.form['email']
	actualizar = f"""
            UPDATE customer
            SET first_name = '{first_name}', last_name = '{last_name}', email = '{email}'
            WHERE customer_id = {id};
        """

	# Update the data in the table 
	cur.execute(actualizar)

	# commit the changes 
	conn.commit()
	
	# close the cursor and connection 
	cur.close() 
	conn.close() 
	return redirect(url_for('customer')) 


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
	id = request.form['customer_id'] 

	# Delete the data from the table 
	cur.execute(f"DELETE FROM customer WHERE customer_id={id}") 

	# commit the changes 
	conn.commit() 

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return redirect(url_for('customer')) 
