from flask import render_template


def index(): 
    # Greet the user 
	return render_template('home_view.html') 