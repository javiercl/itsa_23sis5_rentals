#equipo: 10_ modelo store
#alfonso nuñez esquivel y juan jose nuñez esquivel
from flask import jsonify, render_template, request, redirect, url_for, g, current_app
from flask_paginate import Pagination, get_page_parameter
import psycopg2
import logging

def index(page):

    with current_app.app_context():
        db = current_app.db
        user = current_app.user
        passw = current_app.passw
        server = current_app.server

    logging.basicConfig(level=logging.DEBUG)

    # Connect to the database
    conn = psycopg2.connect(database=db, user=user, password=passw, host=server, port="5432")

    cur = conn.cursor()
    cur.execute(f"SELECT count(*) from store")  # Assuming 'store' is the correct table name
    datax = cur.fetchall()
    data2 = datax[0][0]  # Number of records found in the table

    page = request.args.get(get_page_parameter(), type=int, default=int(page))
    offset = (page - 1) * 20

    cur.execute(f"SELECT s.store_id, s.manager_staff_id, s.address_id, s.last_update, st.first_name, st.last_name, a.address, a.address2, a.district, a.city_id, a.postal_code, a.phone FROM store s, staff st, address a WHERE s.manager_staff_id = st.staff_id AND s.address_id = a.address_id ORDER BY s.store_id LIMIT 20 OFFSET {offset}")
    datax = cur.fetchall()

    pagination = Pagination(page=page, data=datax, total=data2, css_framework='bootstrap4', record_name='store')

    # Select all products from the '' table
    cur.execute('''SELECT address_id, title FROM film ORDER BY title''')
    pelis = cur.fetchall()

    # Select all products from the '' table
    cur.execute('''SELECT manager_staff_id, name FROM category ORDER BY name''')
    categs = cur.fetchall()

    # Close the cursor and connection
    cur.close()
    conn.close()

    return render_template('store_view.html', data=datax, pagination=pagination, pelis=pelis, categs=categs)


def create():
    with current_app.app_context():
        db = current_app.db
        user = current_app.user
        passw = current_app.passw
        server = current_app.server

    # Connect to the database
    conn = psycopg2.connect(database=db, user=user, password=passw, host=server, port="5432")
    cur = conn.cursor()

    # Obtain data from the form
    store_id = request.form['store_id']
    manager_staff_id = request.form['manager_staff_id']
    address_id = request.form['address_id']

    # Insert the new record into the 'store' table
    cur.execute("INSERT INTO store (store_id, manager_staff_id, address_id) VALUES (%s, %s, %s)",
                (store_id, manager_staff_id, address_id))

    # Commit the changes and close the connection
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('store'))


def update():
    with current_app.app_context():
        db = current_app.db
        user = current_app.user
        passw = current_app.passw
        server = current_app.server

    # Connect to the database
    conn = psycopg2.connect(database=db, user=user, password=passw, host=server, port="5432")
    cur = conn.cursor()

    # Get data from the form
    store_id = request.form['store_id']
    manager_staff_id = request.form['manager_staff_id']
    address_id = request.form['address_id']

    # Update the data in the 'store' table
    cur.execute("UPDATE store SET manager_staff_id=%s, address_id=%s WHERE store_id=%s",
                (manager_staff_id, address_id, store_id))

    # Commit the changes and close the connection
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('store'))


def delete():
    with current_app.app_context():
        db = current_app.db
        user = current_app.user
        passw = current_app.passw
        server = current_app.server

    # Connect to the database
    conn = psycopg2.connect(database=db, user=user, password=passw, host=server, port="5432")
    cur = conn.cursor()

    # Get data from the form
    store_id = request.form['store_id']

    # Delete the record from the 'store' table
    cur.execute("DELETE FROM store WHERE store_id=%s", (store_id,))

    # Commit the changes and close the connection
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('store'))
