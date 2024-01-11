from flask import Flask, render_template, request, redirect, url_for 
import psycopg2 

app = Flask(__name__) 

db = 'dvdrental'
user = 'postgres'
server = 'database-instance-tallerbd.ccuu52uctcpx.us-west-2.rds.amazonaws.com'

#Maria Guadalupe Molontzin Ruiz
#equipo 6
#tabla countries

#inicio - Leer el password desde archivo
#f=open("passwd.txt","r")
#lines=f.readlines()
passw="Jacl1234#"
#f.close()
#fin - Leer el password desde archivo


@app.route('/') 
def index(): 
	# Connect to the database 
	conn = psycopg2.connect(database=db, 
							user=user, 
							password=passw, 
							host=server, port="5432") 

	# create a cursor 
	cur = conn.cursor() 

	# Select all products from the table 
	cur.execute('''SELECT * FROM country''') 

	# Fetch the data 
	datax = cur.fetchall() 

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return render_template('country.html', data=datax) 


@app.route('/create', methods=['POST']) 
def create(): 
	# Connect to the database 
	conn = psycopg2.connect(database=db, 
							user=user, 
							password=passw, 
							host=server, port="5432") 

	cur = conn.cursor() 

	# Get the data from the form 
	country = request.form['country'] 

	# Insert the data into the table 
	cur.execute(f"INSERT INTO country (country) VALUES ('{country}')") 

	# commit the changes 
	conn.commit() 

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return redirect(url_for('index')) 


@app.route('/update', methods=['POST']) 
def update(): 
	# Connect to the database 
	conn = psycopg2.connect(database=db, 
							user=user, 
							password=passw, 
							host=server, port="5432") 

	cur = conn.cursor() 

	# Get the data from the form 
	country = request.form['country'] 
	id = request.form['country_id'] 

	# Update the data in the table 
	cur.execute(f"UPDATE country SET country='{country}' WHERE country_id={id}")

	# commit the changes 
	conn.commit() 
	return redirect(url_for('index')) 


@app.route('/delete', methods=['POST']) 
def delete(): 
	# Connect to the database 
	conn = psycopg2.connect(database=db, 
							user=user, 
							password=passw, 
							host=server, port="5432") 
	cur = conn.cursor() 

	# Get the data from the form 
	id = request.form['country_id'] 

	# Delete the data from the table 
	cur.execute(f"DELETE FROM country WHERE country_id={id}") 

	# commit the changes 
	conn.commit() 

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return redirect(url_for('index')) 


if __name__ == '_main_': 
	app.run(debug=True)