from flask import Blueprint

blueprint = Blueprint('blueprint', __name__)

from app import routes, models