from flask import render_template, request, redirect, url_for, g, current_app
from flask_paginate import Pagination, get_page_parameter
import psycopg2
import logging
'''
TABLA DE PAYMENT
EQUIPO 11
ANGEL VENEGAS HERNANDEZ
MONSERRAT NARANJO MERCADO
'''
def index(page3):

	with current_app.app_context():
		db = current_app.db
		user = current_app.user
		passw = current_app.passw
		server = current_app.server
  
	logging.basicConfig(level=logging.DEBUG)
	
	
   	# Connect to the database 
	conn = psycopg2.connect(database=db, user=user, password=passw, host=server, port="5432") 

	cur = conn.cursor() 
	cur.execute(f"SELECT count(*) from payment") 
	datax = cur.fetchall()
	data2 = datax[0][0] # numero de registros encontrados en la tabla
 
	page3 = request.args.get(get_page_parameter(), type=int, default=int(page3))
	if(page3 == 1):
		cur = conn.cursor() 
		cur.execute(f"SELECT p.payment_id, c.first_name ||' '|| c.last_name, s.first_name ||' '|| s.last_name, p.rental_id, p.amount, p.customer_id, p.staff_id FROM payment p, staff s, customer c, rental r WHERE p.customer_id=c.customer_id and p.staff_id=s.staff_id and r.rental_id=p.rental_id order by p.payment_id desc OFFSET 0 LIMIT 50;") 
		datax = cur.fetchall()
	else:
		cur = conn.cursor() 
		cur.execute(f"SELECT p.payment_id, c.first_name ||' '|| c.last_name, s.first_name ||' '|| s.last_name, p.rental_id, p.amount, p.customer_id, p.staff_id FROM payment p, staff s, customer c, rental r WHERE p.customer_id=c.customer_id and p.staff_id=s.staff_id and r.rental_id=p.rental_id order by p.payment_id desc LIMIT {20} offset { 20 * int(page3)};") 
		datax = cur.fetchall()

	pagination = Pagination(page=page3, data=datax, total=data2, css_framework='bootstrap4', record_name='payment')

	# Select all products from the table 
	cur.execute('''select staff_id, first_name ||' '|| last_name  from staff order by staff_id asc''') 
	# Fetch the data 
	staffs = cur.fetchall()
    # Select all products from the table 
	cur.execute('''select customer_id, first_name ||' '|| last_name from customer order by customer_id asc''') 
	# Fetch the data 
	customers = cur.fetchall()
	cur.execute('''select rental_id from rental order by rental_id asc''') 
	# Fetch the data 
	rental = cur.fetchall()
	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return render_template('payment_view.html', data=datax, pagination=pagination, staffs=staffs,customers=customers, rentas=rental) 

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
	customer_id = request.form['crear_pago'] 
	staff = request.form['crear_staff'] 
	renta = request.form['crear_renta'] 
	precio = request.form['precio'] 
	# Insert the data into the table 
	cur.execute(f" INSERT INTO payment (customer_id, staff_id, rental_id, amount, payment_date) VALUES ({customer_id}, {staff}, {renta}, {precio}, now());") 
    
	# commit the changes 
	conn.commit() 

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return redirect(url_for('payment')) 



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
	customer_id = request.form['customer_id'] 
	staff_id = request.form['staff_id'] 
	payment_id=request.form['payment_id']

	# Update the data in the table 
	cur.execute(f"UPDATE payment SET customer_id='{customer_id}', staff_id='{staff_id}' WHERE payment_id={payment_id}")

	# commit the changes 
	conn.commit() 
	cur.close() 
	conn.close() 
	return redirect(url_for('payment')) 


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
	payment_id = request.form['payment_id'] 

	# Delete the data from the table 
	cur.execute(f"DELETE FROM payment WHERE payment_id={payment_id}") 

	# commit the changes 
	conn.commit() 

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return redirect(url_for('payment')) 
