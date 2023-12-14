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
app.add_url_rule('/category','category', category.index)
app.add_url_rule('/film_category','film_category', film_category.index)


if __name__ == '__main__': 
	app.run(debug=True) 
