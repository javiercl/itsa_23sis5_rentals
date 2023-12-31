from flask import Flask, current_app
import home, category, film_category,language,film,inventory, customer, payment, address

app = Flask(__name__) 

#inicio - Leer el password desde archivo
f=open("passwd.txt","r")
lines=f.readlines()
f.close()
#fin - Leer el password desde archivo

with app.app_context():
	current_app.db = 'dvdrental'
	current_app.user = 'postgres'
	current_app.server = 'database-instance-tallerbd.ccuu52uctcpx.us-west-2.rds.amazonaws.com'
	current_app.passw=lines[0]

app.add_url_rule('/','home', home.index)

app.add_url_rule('/category','category', category.index, methods = ['GET'])
app.add_url_rule('/category/create','category_create', category.create, methods = ['POST'])
app.add_url_rule('/category/update','category_update', category.update, methods = ['POST'])
app.add_url_rule('/category/delete','category_delete', category.delete, methods = ['POST'])


app.add_url_rule('/film_category','film_category', film_category.index, defaults={'page': 1}, methods = ['GET'])

app.add_url_rule('/film_category/<page>','film_category', film_category.index, methods = ['GET'])
app.add_url_rule('/film_category/create','film_category_create', film_category.create, methods = ['POST'])
app.add_url_rule('/film_category/update','film_category_update', film_category.update, methods = ['POST'])
app.add_url_rule('/film_category/delete','film_category_delete', film_category.delete, methods = ['POST'])

app.add_url_rule('/film','film_view', film.index, methods = ['GET'])
app.add_url_rule('/film/search','film_search', film.search, methods = ['POST'])
app.add_url_rule('/film/create','film_create', film.create, methods = ['POST'])
app.add_url_rule('/film/update','film_update', film.update, methods = ['POST'])
app.add_url_rule('/film/delete','film_delete', film.delete, methods = ['POST'])
#Modificacion en la clase lenguaje
app.add_url_rule('/language','language_view', language.index, methods = ['GET'])
app.add_url_rule('/language/create','language_create', language.create, methods = ['POST'])
app.add_url_rule('/language/update','language_update', language.update, methods = ['POST'])
app.add_url_rule('/language/delete','language_delete', language.delete, methods = ['POST'])

app.add_url_rule('/inventory','inventory', inventory.index, defaults={'page2': 1}, methods = ['GET'])
app.add_url_rule('/inventory/<page2>','inventory', inventory.index, methods = ['GET'])
app.add_url_rule('/inventory/create','inventory_create', inventory.create, methods = ['POST'])
app.add_url_rule('/inventory/update','inventory_update', inventory.update, methods = ['POST'])
app.add_url_rule('/inventory/delete','inventory_delete', inventory.delete, methods = ['POST'])

app.add_url_rule('/customer','customer_view', customer.index, methods = ['GET'])
app.add_url_rule('/customer/create','customer_create', customer.create, methods = ['POST'])
app.add_url_rule('/customer/update','customer_update', customer.update, methods = ['POST'])
app.add_url_rule('/customer/delete','customer_delete', customer.delete, methods = ['POST'])

#Tabla payment agregada por el equipo de Angel Venegas Hernández Y Monserrat Naranjo Mercado
app.add_url_rule('/payment','payment', payment.index, defaults={'page3': 1}, methods = ['GET'])
app.add_url_rule('/payment/<page3>','payment', payment.index, methods = ['GET'])
app.add_url_rule('/payment/create','payment_create', payment.create, methods = ['POST'])
app.add_url_rule('/payment/update','payment_update', payment.update, methods = ['POST'])
app.add_url_rule('/payment/delete','payment_delete', payment.delete, methods = ['POST'])


app.add_url_rule('/address','address', address.index, methods = ['GET'])
app.add_url_rule('/address/create','address_create', address.create, methods = ['POST'])
app.add_url_rule('/address/update','address_update', address.update, methods = ['POST'])
app.add_url_rule('/address/delete','address_delete', address.delete, methods = ['POST'])

if __name__ == '__main__': 
	app.run(debug=True) 
