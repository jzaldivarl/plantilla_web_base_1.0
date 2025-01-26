# app/routes/homeBP.py #

# Import necessary modules from Flask
from flask import Blueprint, render_template  # Blueprint to modularize routes, render_template to load templates

# Import login_required from Flask-Login to protect routes (although not used in this file)
from flask_login import login_required  # Requires authentication to access certain views

# Define a blueprint for home routes
homeBp = Blueprint('home', __name__, url_prefix='/home')

# Main route for the blueprint
@homeBp.route('/')
# @login_required  # This decorator can be used if you want to restrict access to authenticated users only
def home():
    """
    Renders the main page of the website (home).
    """
    return render_template('home.html')  # Loads and returns the 'home.html' file



