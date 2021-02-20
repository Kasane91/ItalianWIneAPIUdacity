import os, json
from flask import Flask, request, abort, jsonify, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models.models import setup_db, db_drop, create_all, Wine, District



obj_per_page = 8

def paginate_obj(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page-1) * obj_per_page
    end = start + obj_per_page

    units = [unit.format() for unit in selection]
    return units[start:end]

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)

    ''' UNCOMMENT THE FOLLOWING LINES, IF YOU WISH TO INITIALIZE THE DATABASE FROM SCRATCH - OTHERWISE USE PROVIDED DATABASE DUMP'''
    #create_all()
    #db_drop()


    @app.route('/', methods=['GET'])
    def index():
        return render_template("index.html")

    
    #@TODO CREATE A GET ENDPOINT TO RETRIEVE PAGINATED LISTS OF WINES
    @app.route('/wines', methods=['GET'])
    def get_wines():
        pass

    #@TODO CREATE A GET ENDPOINT TO RETRIEVE LIST OF DISTRICTS
    @app.route('/districts', methods=['GET'])
    def get_districts():
        districts = District.query.all()

        if len(districts) == 0:
            return abort(404, 'Resource not found')
        districts_paginated = paginate_obj(request, districts)

        return jsonify({
            'success': True,
            'districts': districts_paginated
        })


    #@TODO CREATE A GET ENDPOINT TO RETRIEVE LIST OF WINES SORTED BY DISTRICT
    @app.route('/districts/<int:district_id>', methods=['GET'])
    def get_wines_sorted(district_id):
        pass

    
    #@TODO CREATE A POST ENDPOINT TO CREATE A WINE INSTANCE
    @app.route('/wines', methods=['POST'])
    def create_wine():
        pass

    #@TODO CREATEA  POST ENDPOINT TO CREATE A DISTRICT ENTRY
    @app.route('/districts', methods=['POST'])
    def create_district():
        body = request.get_json()
        if not body: abort(422, 'Unprocessable entry')

        district_data = {
            'name': body.get('name'),
            'province': body.get('province')
        }

        district = District(**district_data)
        district.insert()

        return jsonify({
            'success': True,
            'created': district.format()
        })



    #@TODO CREATE A DELETE ENDPOINT TO REMOVE WINE BY ID
    @app.route('/wines/<int:wine_id>', methods=['DELETE'])
    def delete_wine(wine_id):
        pass

    #@TODO CREATE A DELETE ENDPOINT TO REMOVE DISTRICT BY ID
    @app.route('/districts/<int:district_id>', methods=['DELETE'])
    def delete_district(district_id):
        pass

    #@TODO CREATE A PATCH ENDPOINT TO EDIT WINE RATING:
    @app.route('/wines/<int:wine_id>', methods=['PATCH'])
    def edit_wine(wine_id):
        pass

    #@TODO CREATE A PATCH ENDPOINT TO EDIT DISTRICT PARAMETERS
    @app.route('/district/<int:district_id>', methods=['PATCH'])
    def edit_district(district_id):
        pass













    return app

app = create_app()
