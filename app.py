from flask import Flask, current_app
import home, category, film_category

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


if __name__ == '__main__': 
	app.run(debug=True) 
