from flask import Flask, render_template, request, redirect, url_for 
import psycopg2 

app = Flask(__name__) 

db = 'dvdrental'
user = 'postgres'
server = 'database-instance-tallerbd.ccuu52uctcpx.us-west-2.rds.amazonaws.com'

#inicio - Leer el password desde archivo
f=open("passwd.txt","r")
lines=f.readlines()
passw=lines[0]
f.close()
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
	cur.execute('''SELECT * FROM category''') 

	# Fetch the data 
	datax = cur.fetchall() 

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return render_template('index.html', data=datax) 


@app.route('/create', methods=['POST']) 
def create(): 
	# Connect to the database 
	conn = psycopg2.connect(database=db, 
							user=user, 
							password=passw, 
							host=server, port="5432") 

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
	name = request.form['name'] 
	id = request.form['category_id'] 

	# Update the data in the table 
	cur.execute(f"UPDATE category SET name='{name}' WHERE category_id={id}")

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
	id = request.form['category_id'] 

	# Delete the data from the table 
	cur.execute(f"DELETE FROM category WHERE category_id={id}") 

	# commit the changes 
	conn.commit() 

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return redirect(url_for('index')) 


if __name__ == '__main__': 
	app.run(debug=True) 
