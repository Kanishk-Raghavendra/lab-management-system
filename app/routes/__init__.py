from flask import Blueprint

# We create the Blueprint object here
# 'main_routes' is the name we'll use to reference it
main_routes_blueprint = Blueprint('main_routes', __name__)

# We import the routes from main.py *after* creating the blueprint
# to avoid circular import errors.
from . import main