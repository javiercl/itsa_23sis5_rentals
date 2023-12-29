from flask import render_template, request, redirect, url_for, g, current_app
import psycopg2 
#?imagen del esquema de la base de datos
#? https://www.postgresqltutorial.com/wp-content/uploads/2018/03/dvd-rental-sample-database-diagram.png
'''
	Walter Jahir Ambriz Reyna 21020041
	Ana Laura Cortez Cortes
	Daniel Alejandro Gonzalez Rodriguez
'''
def search():
    with current_app.app_context():
        db = current_app.db
        user = current_app.user
        passw = current_app.passw
        server = current_app.server

    # Connect to the database 
    conn = psycopg2.connect(database=db, user=user, password=passw, host=server, port="5432")

    # create a cursor 
    cur = conn.cursor() 

    # Cambia de request.form a request.args
    name = request.form['buscar']

    print(f"Valor de 'name' recibido: {name}")

    busqueda =  f'''
    SELECT film.film_id, film.title, film.release_year, language.name AS language, category.name AS category, 
    film.description, CONCAT((film.length / 60)::int, 'h ', (film.length % 60)::int, 'min') AS duration, 
    film.rental_duration, film.rental_rate, film.replacement_cost, film.rating, film.special_features 
    FROM film 
    JOIN language ON film.language_id = language.language_id 
    JOIN film_category ON film.film_id = film_category.film_id 
    JOIN category ON film_category.category_id = category.category_id 
    WHERE LOWER(film.title) LIKE LOWER('%{name}%');
    '''

    # Select all products from the table
    cur.execute(busqueda)
    # Fetch the data 
    datax = cur.fetchall()
    cur.execute("SELECT language_id,name AS language FROM language;")
    idems = cur.fetchall()

    cur.execute("SELECT film.film_id, category.name AS category FROM film JOIN film_category ON film.film_id = film_category.film_id JOIN category ON film_category.category_id = category.category_id;")
    category = cur.fetchall()

    # close the cursor and connection 
    cur.close() 
    conn.close() 

    return render_template('film_view.html', data=datax, idems=idems, category=category)


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
	cur.execute("SELECT film.film_id, film.title, film.release_year, language.name AS language, category.name AS category, film.description, CONCAT((film.length / 60)::int, 'h ', (film.length % 60)::int, 'min') AS duration, film.rental_duration, film.rental_rate, film.replacement_cost, film.rating, film.special_features FROM film JOIN language ON film.language_id = language.language_id JOIN film_category ON film.film_id = film_category.film_id JOIN category ON film_category.category_id = category.category_id LIMIT 5;")
	# Fetch the data 
	datax = cur.fetchall()

	cur.execute("SELECT language_id,name AS language FROM language;")
	idems = cur.fetchall()

	cur.execute("SELECT film.film_id, category.name AS category FROM film JOIN film_category ON film.film_id = film_category.film_id JOIN category ON film_category.category_id = category.category_id;")
	category = cur.fetchall()

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return render_template('film_view.html', data=datax,idems=idems, category=category) 

def create():
    with current_app.app_context():
        db = current_app.db
        user = current_app.user
        passw = current_app.passw
        server = current_app.server

    # Obtener los datos del formulario
    name = request.form['title']
    des = request.form['description']
    rele_year = request.form['release_year']
    id_lang = request.form['numero']
    durationr = request.form['rental_duration']
    r_r = request.form['rental_rate']
    duration = request.form['length']
    r_cost = request.form['replacement_cost']
    rating = request.form['rating']
    esp_feat = request.form['special_features']
    category_id = request.form['category_id']

    # Crear una lista de características especiales como una cadena
    special_features_str = "ARRAY['" + "', '".join(esp_feat.split(',')) + "']"

    # Construir y ejecutar la instrucción SQL INSERT
    insert = f"""
        INSERT INTO film (title, description, release_year, language_id, rental_duration, rental_rate, 
                        length, replacement_cost, rating, special_features)
        VALUES ('{name}', '{des}', {rele_year}, {id_lang}, {durationr}, {r_r}, {duration}, 
                {r_cost}, '{rating}', {special_features_str})
        RETURNING film_id;
    """

    # Connect to the database 
    conn = psycopg2.connect(database=db, user=user, password=passw, host=server, port="5432")
    cur = conn.cursor()

    # Ejecutar la instrucción SQL para insertar en la tabla film y obtener el film_id
    cur.execute(insert)
    film_id = cur.fetchone()[0]

    # Construir y ejecutar la instrucción SQL para insertar en la tabla film_category
    insert_category = f"""
        INSERT INTO film_category (film_id, category_id)
        VALUES ({film_id}, {category_id});
    """
    cur.execute(insert_category)

    # Confirmar los cambios en la base de datos
    conn.commit()

    # Cerrar el cursor y la conexión 
    cur.close() 
    conn.close() 

    return redirect(url_for('film'))



def update():
    
	with current_app.app_context():
		db = current_app.db
		user = current_app.user
		passw = current_app.passw
		server = current_app.server
 
	# Connect to the database 
	conn = psycopg2.connect(database=db, user=user, password=passw, host=server, port="5432")

	cur = conn.cursor() 

	# Get the data from the update form
	film_id = request.form['id_film']
	title = request.form['title']
	category_id = request.form['category_id']
	descrip = request.form['descrip']
	release_year = request.form['release_year']
	id_lang = request.form['id_lang']
	rental_duration = request.form['rental_duration']
	rental_rate = request.form['rental_rate']
	length = request.form['length']
	replacement_cost = request.form['replacement_cost']
	rating = request.form['rating']
	special_features = request.form['special_features']

	special_features_str = "ARRAY['" + "', '".join(special_features.split(',')) + "']"

	act = f'''
	UPDATE film
	SET
	title = '{title}',
	description = '{descrip}',
	release_year = {release_year},
	language_id = {id_lang},
	rental_duration = {rental_duration},
	rental_rate = {rental_rate},
	length = {length},
	replacement_cost = {replacement_cost},
	rating = '{rating}',
	last_update = NOW(),
	special_features = ARRAY[{special_features_str}]
	FROM film_category
	WHERE film.film_id = film_category.film_id
	AND film.film_id = {film_id};

	UPDATE film_category
	SET category_id = {category_id}
	WHERE film_id = {film_id};
	'''
	# Update the data in the table 
	cur.execute(act)
	# commit the changes
	conn.commit() 
	# close the cursor and connection 
	cur.close() 
	conn.close() 
	return redirect(url_for('film')) 


def delete():
    
	with current_app.app_context():
		db = current_app.db
		user = current_app.user
		passw = current_app.passw
		server = current_app.server
 
	# Connect to the database 
	conn = psycopg2.connect(database=db, user=user, password=passw, host=server, port="5432")
	#conn = psycopg2.connect(**params)
	cur = conn.cursor() 

	# Get the data from the form 
	id = request.form['film_id'] 

	# Delete the data from the table 
	delete = f'''
		DELETE FROM film_actor WHERE film_id = {id};
		DELETE FROM film_category WHERE film_id = {id};
		DELETE FROM inventory WHERE film_id = {id};
		DELETE FROM film WHERE film_id = {id};
	'''
	cur.execute(delete) 

	# commit the changes
	conn.commit() 

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return redirect(url_for('film')) 
