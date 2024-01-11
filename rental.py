''' EQUIPO 7:
		LUIS FRANCISCO MENDOZA ROSAS
		ALFREDO GASCA RAMIREZ
		LUIS ENRIQUE TORRES CERVANTES
'''
from flask import render_template, request, redirect, url_for, g, current_app
from flask_paginate import Pagination, get_page_parameter
import psycopg2
import logging

def index(indexpag): 
    # Connect to the database 
	with current_app.app_context():		
		db = current_app.db				
		user = current_app.user			
		passw = current_app.passw		
		server = current_app.server		

	logging.basicConfig(level=logging.DEBUG)

	''' --- CONFIGURE THE CONNECTION --- '''
	conn = psycopg2.connect(
		database=db, host=server, port="5432",
		user=user, password=passw) 
	cur = conn.cursor() 

	cur.execute(f"SELECT count(*) from rental")
	results = cur.fetchall(); # Fetch how many registers on rental
	totaldata = results[0][0];	# Used later for stuff

	paginas = request.args.get(get_page_parameter(), type=int, default=int(indexpag))
	if(paginas == 1):
		cur = conn.cursor() 
		cur.execute(
			f'''SELECT 	R.rental_id, R.inventory_id, S.first_name, C.first_name, C.customer_id, 
	 					R.rental_date, R.return_date, R.last_update
	 			FROM rental R, customer C, staff S 
	 			WHERE R.customer_id = C.customer_id AND R.staff_id = S.staff_id
				ORDER BY rental_id ASC
				limit {40} offset {0}
     		''') 
		results = cur.fetchall()
	else:
		cur = conn.cursor() 
		cur.execute(
			f'''SELECT 	R.rental_id, R.inventory_id, S.first_name, C.first_name, C.customer_id, 
	 					R.rental_date, R.return_date, R.last_update
	 			FROM rental R, customer C, staff S 
	 			WHERE R.customer_id = C.customer_id AND R.staff_id = S.staff_id
				ORDER BY rental_id ASC
				LIMIT {20} offset {20 * int(paginas)}''')
		results = cur.fetchall()
     
	pagination = Pagination(page=paginas, data=results, total=totaldata, css_framework='bootstrap4', record_name='film_category')
	cur.execute('''SELECT DISTINCT first_name FROM staff ORDER BY first_name'''); staffFN = cur.fetchall(); # Get all staff names
	cur.execute('''SELECT DISTINCT staff_id,first_name FROM staff ORDER BY staff_id'''); staffID = cur.fetchall(); # Get [0]StaffID-[1]StaffFirstName
	cur.execute('''SELECT DISTINCT customer_id,first_name FROM customer ORDER BY customer_id'''); customerIDFN = cur.fetchall(); # Get [0]customerID-[1]CustomerName
	cur.execute('''SELECT DISTINCT first_name FROM customer ORDER BY first_name'''); customerFN = cur.fetchall(); # Get all customer's names 
	cur.execute('''SELECT DISTINCT inventory_id FROM inventory ORDER BY inventory_id'''); invID = cur.fetchall(); # Get all inventory items 


	cur.close(); conn.close(); # close the cursor and connection 
	return render_template('rental_view.html', data=results, pagination=pagination, #Render the template rental_view
	CB_staff_name=staffFN, CB_staffID=staffID, CB_cust_id=customerIDFN, CB_CFirstName=customerIDFN, CB_invID=invID) 

def create():
	with current_app.app_context():
		db = current_app.db
		user = current_app.user
		passw = current_app.passw
		server = current_app.server

	# Connect to the database 
	conn = psycopg2.connect(
		database=db, host=server, port="5432",
		user=user, password=passw, 
	) 
	cur = conn.cursor() 

	# Get the data from the form 
	custid = request.form['c_customer_id']; #get customerID
	invid = request.form['c_inventory_id']; #get inventoryID
	stid = request.form['c_staff_id']; #get staffID
	
	# Insert the data into the table 
	cur.execute(
		f'''INSERT INTO rental (staff_id,rental_date,inventory_id,customer_id,return_date) 
			VALUES ({stid},now(),{invid},{custid},CURRENT_TIMESTAMP+interval '30 days')
		'''
	) 
	conn.commit(); cur.close(); conn.close(); # close the cursor and connection 

	return redirect(url_for('rental')) 

def update():     	
	with current_app.app_context():
		db = current_app.db
		user = current_app.user
		passw = current_app.passw
		server = current_app.server
	
    # Connect to the database 
	conn = psycopg2.connect(
		database=db, host=server, port="5432",
		user=user, password=passw) 
	cur = conn.cursor() 

	# Get the data from the form 
	cname = request.form['upd_cli_name']; 	## [0] is for id, [1] customer_name
	stname= request.form['upd_staffFN'];	#staff name
	cusid = request.form['upd_cli_id'];		#customer_id
	renid = request.form['upd_ren_id']; 	#rental id
	
	# Update the data in the table 
	cur.execute(
	f'''UPDATE rental SET customer_id={cname} --this is really an id
		WHERE rental_id = {renid};
		--busca el staffID respecto al nombre en la tabla de staff
		UPDATE rental SET staff_id=(select staff_id from staff where first_name='{stname}') 
		WHERE customer_id={cusid} AND rental_id={renid};
	''')

	conn.commit(); # commit the changes 
	return redirect(url_for('rental')) 

def delete(): 
	with current_app.app_context():
		db = current_app.db
		user = current_app.user
		passw = current_app.passw
		server = current_app.server

	# Connect to the database 
	conn = psycopg2.connect(
		database=db, host=server, port="5432",
		user=user, password=passw
	) 
	cur = conn.cursor() 

	# Get the data from the form 
	cliid = request.form['del_cli_id'];	#customer_id
	proid = request.form['del_pro_id'];	#inventory_id

	cur.execute(
		f'''DELETE FROM rental 
			WHERE inventory_id={proid} AND customer_id={cliid}; 
		'''
	) 

	conn.commit(); # commit the changes 
	cur.close(); conn.close(); # close the cursor and connection 
	return redirect(url_for('rental')) 
