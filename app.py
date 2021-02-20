import os
from flask import Flask, request, abort, jsonify, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models.models import setup_db, db_drop, create_all, Wine, District
import json


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    create_all()


    @app.route('/', methods=['GET'])
    def index():
        return render_template("index.html")











    return app

app = create_app()
