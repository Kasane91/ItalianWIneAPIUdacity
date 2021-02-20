import os, json
from flask import Flask, request, abort, jsonify, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models.models import setup_db, db_drop, create_all, Wine, District
from auth.auth import AuthError, requires_auth 
from dotenv import load_dotenv

'''
GENERATE TOKENS:
https://dev-b7i37lqi.eu.auth0.com/authorize?audience=Wine&response_type=token&client_id=f7J8eQZl597jjobhwsF4aT2N6e7IHeYx&redirect_uri=https://italianwineapi.herokuapp.com
'''


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
    cors = CORS(app)

    '''
    UNCOMMENT THE FOLLOWING LINES, IF YOU WISH TO INITIALIZE THE DATABASE FROM SCRATCH - 
    OTHERWISE USE PROVIDED DATABASE DUMP COMMAND:
    createdb italianwine
    psql -d italianwine -U postgres -a -f italianwine.psql

    '''
    #create_all()
    #db_drop()

    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


    @app.route('/', methods=['GET'])
    def index():
        return (os.environ.get)

    
    #@TODO CREATE A GET ENDPOINT TO RETRIEVE PAGINATED LISTS OF WINES
    @app.route('/wines', methods=['GET'])
    def get_wines():
        wines = Wine.query.all()
        if len(wines)==0:
            return abort(404, 'Resource not found. Not a valid district')

        wines_paginated = paginate_obj(request, wines)

        return jsonify({
            'success': True,
            'wines': wines_paginated
        })


    #@TODO CREATE A GET ENDPOINT TO RETRIEVE LIST OF DISTRICTS
    @app.route('/districts', methods=['GET'])
    @requires_auth('get:districts')
    def get_districts(payload):
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
    @requires_auth('get:wines')
    def get_wines_sorted(district_id):
        wine = Wine.query.filter(district_id==district_id).all()
        district = District.query.filter(District.id == district_id).first()

        if len(wine)== 0:
            abort(404, 'Resources not found. Not a valid district')
        
        wine_paginated = paginate_obj(request, wine)

        return jsonify({
            'success': True,
            'wine': wine_paginated,
            'district': district.name
        })
        

    
    #@TODO CREATE A POST ENDPOINT TO CREATE A WINE INSTANCE
    @app.route('/wines', methods=['POST'])
    @requires_auth('post:wines')
    def create_wine(payload):
        body = request.get_json()

        wine_data = {
            'producer': body.get('producer'),
            'vintage': int(body.get('vintage')),
            'grape': body.get('grape'),
            'vinyard': body.get('vinyard'),
            'rating': int(body.get('rating')),
            'district_id': int(body.get('district_id'))
        }
        if 'producer' and 'vintage' and 'grape' and 'district_id' not in wine_data:
            return abort(422, 'Unprocessable entry')
        
        wine = Wine(**wine_data)
        
        wine.insert()

        return jsonify({
            'success': True,
            'wine': wine.format()
        })

    #@TODO CREATEA  POST ENDPOINT TO CREATE A DISTRICT ENTRY
    @app.route('/districts', methods=['POST'])
    @requires_auth('post:districts')
    def create_district(payload):
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
    @requires_auth('delete:wines')
    def delete_wine(payload, wine_id):
        wine = Wine.query.get(wine_id)

        if wine:
            wine.delete()
            return jsonify({
                'success': True,
                'deleted': wine.format()
            })
        else:
            return abort(404, f'Wine with id {wine_id} does not exist')

    #@TODO CREATE A DELETE ENDPOINT TO REMOVE DISTRICT BY ID
    @app.route('/districts/<int:district_id>', methods=['DELETE'])
    @requires_auth('delete:districts')
    def delete_district(payload, district_id):
        district = District.query.get(district_id)

        if district:
            district.delete()
            return jsonify({
                'success': True,
                'deleted': district.format()
            })

    #@TODO CREATE A PATCH ENDPOINT TO EDIT WINE RATING:
    @app.route('/wines/<int:wine_id>', methods=['PATCH'])
    @requires_auth('patch:wines')
    def edit_wine(payload, wine_id):
        wine = Wine.query.get(wine_id)

        if not wine:
            return abort(404, f'Wine with id {wine_id} does not exist')
        
        body = request.get_json()

        producer = body.get('producer')
        wine.producer = producer if producer else wine.producer

        vintage = body.get('vintage')
        wine.vintage = vintage if vintage else wine.vintage

        grape = body.get('grape')
        wine.grape = grape if grape else wine.grape

        vinyard = body.get('vinyard')
        wine.vinyard = vinyard if vinyard else wine.vinyard

        rating = body.get('rating')
        wine.rating = rating if rating else wine.rating

        district = body.get('district_id')
        wine.district_id = district if district else wine.district_id

        wine.update()

        return json({
            'success': True,
            'Wine': wine.format()
        })

    #@TODO CREATE A PATCH ENDPOINT TO EDIT DISTRICT PARAMETERS
    @app.route('/district/<int:district_id>', methods=['PATCH'])
    @requires_auth('patch:districts')
    def edit_district(payload, district_id):
        district = District.query.get(district_id)

        if not district:
            return abort(404, f'District with id {district_id} does not exist')

        body = request.get_json()

        name = body.get('name')    
        district.name = name if name else district.name

        province = body.get('province')
        district.province = province if province else district.province

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        "success": False, 
        "error": 422,
        "message": error.description
        }), 422



    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
        "success": False, 
        "error": 401,
        "message": error.description
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
        "success": False, 
        "error": 403,
        "message": error.description
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
        "success": False, 
        "error": 404,
        "message": error.description
        }), 404


      
    @app.errorhandler(AuthError)
    def handle_auth_error(exception):
        response = jsonify(exception.error)
        response.status_code = exception.status_code
        return response
   












    return app

app = create_app()
