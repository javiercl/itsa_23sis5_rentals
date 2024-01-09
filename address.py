from flask import Flask, render_template, request, redirect, url_for 
import psycopg2 
#YULIANA JANETH RODRIGUEZ BARAJAS
app = Flask(__name__) 

db = 'dvdrental'
user = 'postgres'
server = 'database-instance-tallerbd.ccuu52uctcpx.us-west-2.rds.amazonaws.com'

#inicio - Leer el password desde archivo
#f=open("passwd.txt","r")
#lines=f.readlines()
passw="Jacl1234#"
#f.close()
#fin - Leer el password desde archivo


@app.route('/') 
@app.route('/')
def index():
    conn = psycopg2.connect(database=db, user=user, password=passw, host=server, port="5432")
    cur = conn.cursor()
    cur.execute('''SELECT * FROM address''')
    data = cur.fetchall()

    # Obtener city_ids distintos
    cur.execute('''SELECT DISTINCT city_id FROM address order by city_id asc''')
    city_ids_data = cur.fetchall()
    city_ids = [row[0] for row in city_ids_data]

    cur.close()
    conn.close()
    return render_template('index.html', data=data, city_ids=city_ids)




@app.route('/create', methods=['POST']) 
def create(): 
	# Connect to the database 
	conn = psycopg2.connect(database=db, 
							user=user, 
							password=passw, 
							host=server, port="5432") 

	cur = conn.cursor() 

	# Get the data from the form 
	address = request.form['address'] 
	address2 = request.form['address2'] 
	district = request.form['district']
	city_id = request.form['city_id']
	postal_code = request.form['postal_code']
	phone = request.form['phone']    

	# Insert the data into the table 
	cur.execute(f"INSERT INTO address (address,address2,district,city_id,postal_code,phone) VALUES ('{address}', '{address2}','{district}',{city_id},'{postal_code}','{phone}')") 

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
	address = request.form['address2'] 
	id = request.form['address_id'] 

	# Update the data in the table 
	cur.execute(f"UPDATE address SET address2='{address}' WHERE address_id={id}")

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
	id = request.form['address_id'] 

	# Delete the data from the table 
	cur.execute(f"DELETE FROM address WHERE address_id={id}") 

	# commit the changes 
	conn.commit() 

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return redirect(url_for('index')) 


if __name__ == '__main__': 
	app.run(debug=True) 
