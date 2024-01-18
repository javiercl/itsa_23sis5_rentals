from flask import render_template, request, redirect, url_for, g, current_app
import psycopg2, logging

def index(): 
    # Connect to the database 
    with current_app.app_context():
        db = current_app.db
        user = current_app.user
        passw = current_app.passw
        server = current_app.server

    logging.basicConfig(level=logging.DEBUG)

    conn = psycopg2.connect(
        database=db, user=user, password=passw, 
        host=server, port="5432") 
    cur = conn.cursor() 

    # Select all products from the table 
    cur.execute('''SELECT * FROM staff'''); datax = cur.fetchall() 

    # Get all the columns of staff > [0]StaffID-[1]StaffFirstName-etc
    cur.execute('''SELECT DISTINCT * FROM staff ORDER BY staff_id'''); staffID = cur.fetchall(); 
    cur.execute('''SELECT DISTINCT address_id FROM address ORDER BY address_id;'''); adress = cur.fetchall();
    cur.execute('''SELECT DISTINCT store_id FROM store ORDER BY store_id;'''); store=cur.fetchall();
    cur.execute('''SELECT DISTINCT active FROM staff'''); activo=cur.fetchall();
    cur.close(); conn.close(); # close the cursor and connection 
    return render_template('staff_view.html', data=datax, CB_staffID=staffID, 
    CB_adress=adress, CB_store=store,CB_active=activo
    ) 

def create(): 
    # Connect to the database 
    with current_app.app_context():
        db = current_app.db
        user = current_app.user
        passw = current_app.passw
        server = current_app.server

    logging.basicConfig(level=logging.DEBUG)

    conn = psycopg2.connect(
        database=db, user=user, password=passw, 
        host=server, port="5432"
    ) 
    cur = conn.cursor() 
    c_nombre =      request.form['c_nombre']
    c_apellido =    request.form['c_apellido']
    c_adress =      request.form['c_adress']
    c_email =       request.form['c_email']   
    c_storeid =     request.form['c_storeid']
    c_active =      request.form['c_active']
    c_username =    request.form['c_username']
    c_password =    request.form['c_password']
    
    # Insert the data into the table 
    cur.execute(
    f'''INSERT INTO 
    staff  (first_name,  last_name,     email,      address_id,store_id,   active,    username,      password,    last_update) 
    VALUES ('{c_nombre}','{c_apellido}','{c_email}',{c_adress},{c_storeid},{c_active},'{c_username}','{c_password}',now());
    ''') 
   
    #close cursor and connection 
    conn.commit(); cur.close(); conn.close() 
    return redirect(url_for('staff')) 

def update(): 
    # Connect to the database 
    with current_app.app_context():
        db = current_app.db
        user = current_app.user
        passw = current_app.passw
        server = current_app.server

    logging.basicConfig(level=logging.DEBUG)

    conn = psycopg2.connect(
        database=db, user=user, password=passw, 
        host=server, port="5432"
    ) 
    cur = conn.cursor() 
    staffFN = request.form.get('staff_fn'); #nombre
    staffLN = request.form.get('staff_ln'); #apellido
    staffAI = request.form.get('staff_ai'); #adress id /// sale none
    staffEM = request.form.get('staff_em'); #email
    staffSI = request.form.get('staff_si'); #store id
    staffAC = request.form.get('staff_ac'); #activo (que cojones es none?)
    staff_ac= 't' if bool(staffAC) is True else 'f'
    staffUN = request.form.get('staff_un'); #username
    staffPA = request.form.get('staff_pa'); #contrasena
    staffUpdT1 = request.form.get('upd_staff_id');  #staff id
    staffUpdT2 = request.form.get('upd2_staff_id'); #staff id

    # Update the data in the table 
    cur.execute(
        f'''UPDATE staff SET first_name='{staffFN}', last_name='{staffLN}', 
            address_id={staffAI}, email='{staffEM}', store_id={staffSI},
            active='{staff_ac}', username='{staffUN}', password='{staffPA}', last_update=now()
            WHERE staff_id={staffUpdT1}
        ''')

    # commit the changes 
    conn.commit() 
    return redirect(url_for('staff')) 

def delete(): 
        # Connect to the database 
    with current_app.app_context():
        db = current_app.db
        user = current_app.user
        passw = current_app.passw
        server = current_app.server

    logging.basicConfig(level=logging.DEBUG)

    #Conexion con la base de datos
    conn = psycopg2.connect(
        database=db, user=user, password=passw, 
        host=server, port="5432") 
    cur = conn.cursor() 

    staffDelT1 = request.form['del_staff_id'];  #staff id
    
    #Borra la informacion de la tabla
    cur.execute(
    f'''DELETE FROM staff 
        WHERE staff_id={staffDelT1}
    ''') 

    #Aqui se cierra la conexion ademas del cursor
    conn.commit(); cur.close(); conn.close()
    return redirect(url_for('staff')) 

'''
    staffFN = request.form['staff_fn']; #nombre
    staffLN = request.form['staff_ln']; #apellido
    staffAI = request.form['staff_ai']; #adress id
    staffEM = request.form['staff_em']; #email
    staffSI = request.form['staff_si']; #store id
    staffAC = request.form['staff_ac']; #activo
    staffUN = request.form['staff_un']; #username
    staffPA = request.form['staff_pa']; #contrasena
    staffUpdT1 = request.form['upd_staff_id'];  #staff id
    staffUpdT2 = request.form['upd2_staff_id']; #staff id
    staffDelT1 = request.form['del_staff_id'];  #staff id
    staffDelT2 = request.form['del2_staff_id']; #staff id
    c_nombre =      request.form['c_nombre']
    c_apellido =    request.form['c_apellido']
    c_adress =      request.form['c_adress']
    c_email =       request.form['c_email']   
    c_storeid =     request.form['c_storeid']
    c_active =      request.form['c_active']
    c_username =    request.form['c_username']
    c_password =    request.form['c_password']
'''
