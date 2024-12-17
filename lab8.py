from flask import Blueprint, render_template, abort, request, jsonify
from random import randint
import psycopg2
from psycopg2.extras import RealDictCursor

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def main():
    return render_template('lab8/lab8.html')