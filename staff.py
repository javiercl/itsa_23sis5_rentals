from flask import Flask, render_template, request, redirect, url_for 
import psycopg2 
import base64

app = Flask(__name__) 

db = 'dvdrental'
user = 'postgres'
server = 'database-instance-tallerdb2.cmrkck6hngna.us-east-2.rds.amazonaws.com'

# Inicio - Leer el password desde archivo
f=open("passwd.txt","r")
lines=f.readlines()
passw=lines[0]
f.close()
# Fin - Leer el password desde archivo

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
    cur.execute('''SELECT * FROM staff''') 

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
    cur.execute(f"INSERT INTO staff (name) VALUES ('{name}')") 

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
    id = request.form['staff_id'] 
    active = request.form['active']
    password = request.form['password']
    last_update = request.form['last_update']
    email = request.form['email']  # Nueva línea para obtener el valor de 'email'
    username = request.form['username']  # Nueva línea para obtener el valor de 'username'

    # Update the data in the table 
    cur.execute(f"UPDATE staff SET name='{name}', active={active}, password='{password}', last_update='{last_update}', email='{email}', username='{username}' WHERE staff_id={id}")

    # commit the changes 
    conn.commit() 
    return redirect(url_for('index')) 

@app.route('/delete', methods=['POST']) 
def delete(): 
    #Conexion con la base de datos
    conn = psycopg2.connect(database=db, 
                            user=user, 
                            password=passw, 
                            host=server, port="5432") 
    cur = conn.cursor() 

    #Recolecta informacion basicamente 
    id = request.form['staff_id'] 

    #Borra la informacion de la tabla
    cur.execute(f"DELETE FROM staff WHERE staff_id={id}") 

    #Aqui se cierra la conexion ademas del cursor
    cur.close() 
    conn.close()
    conn.commit() 

    return redirect(url_for('index')) 

if __name__ == '__main__': 
    app.run(debug=True)