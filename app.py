import os
import json
from flask import (
    Flask,
    request,
    abort, jsonify,
    render_template,
    url_for)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models.models import (
    setup_db,
    db_drop,
    create_all,
    Wine,
    District)
from auth.auth import (
    AuthError,
    requires_auth)
from dotenv import load_dotenv

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
    Uncomment the lines below __IF__ you wish to intitialize the database
    from scratch.
    However it is recommended  use the provided database:
    createdb italianwine
    psql italianwine < italianwine.psql
    OR
    psql -d italianwine -U postgres -a -f italianwine.psql
    '''
    # create_all()
    # db_drop()

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, PATCH, DELETE, OPTIONS')
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    @app.route('/', methods=['GET'])
    def index():

        return jsonify({
            'description': "LIVE - Italian Wine API. See docs for usage"
            })

    @app.route('/wines', methods=['GET'])
    @requires_auth('get:wines')
    def get_wines(payload):
        wines = Wine.query.all()

        wines_paginated = paginate_obj(request, wines)
        if len(wines_paginated) == 0:
            return abort(404, 'Resource not found. Not a valid district')

        return jsonify({
            'success': True,
            'wines': wines_paginated
        })

    @app.route('/wines/<int:wine_id>', methods=['GET'])
    @requires_auth('get:wines')
    def get_wines_by_id(payload, wine_id):
        wine = Wine.query.get(wine_id)
        if not wine:
            return abort(404, "Wine does not exist")

        return jsonify({
            'success': True,
            'wine': wine.format()
        })

    @app.route('/districts', methods=['GET'])
    @requires_auth('get:districts')
    def get_districts(payload):
        districts = District.query.all()

        districts_paginated = paginate_obj(request, districts)
        if len(districts_paginated) == 0:
            return abort(404, 'Resource not found')

        return jsonify({
            'success': True,
            'districts': districts_paginated
        })

    @app.route('/districts/<int:district_id>', methods=['GET'])
    @requires_auth('get:wines')
    def get_wines_sorted(payload, district_id):

        wine = Wine.query.filter(district_id == district_id).all()
        district = District.query.filter(District.id == district_id).first()

        if district is None:
            abort(404, "Resource not found. Not a valdid district")

        wine_paginated = paginate_obj(request, wine)
        if len(wine_paginated) == 0:
            abort(404, 'Resources not found. No wines in district')

        return jsonify({
            'success': True,
            'wine': wine_paginated,
            'district': district.name
        })

    @app.route('/wines', methods=['POST'])
    @requires_auth('post:wines')
    def create_wine(payload):
        body = request.get_json()

        wine_data = {
            'producer': body.get('producer'),
            'vintage': body.get('vintage'),
            'grape': body.get('grape'),
            'vinyard': body.get('vinyard'),
            'rating': body.get('rating'),
            'district_id': body.get('district_id')
        }
        try:
            wine = Wine(**wine_data)
            wine.insert()
        except Exception as e:
            print(e)
            return abort(422, "Incomplete body")

        return jsonify({
            'success': True,
            'wine': wine.format()
        })

    @app.route('/districts', methods=['POST'])
    @requires_auth('post:districts')
    def create_district(payload):
        body = request.get_json()

        district_data = {
            'name': body.get('name'),
            'province': body.get('province')
        }
        try:
            district = District(**district_data)
            district.insert()
        except Exception as e:
            print(e)
            return abort(422, "Incomplete body")

        return jsonify({
            'success': True,
            'created': district.format()
        })

    @app.route('/wines/<int:wine_id>', methods=['DELETE'])
    @requires_auth('delete:wines')
    def delete_wine(payload, wine_id):
        wine = Wine.query.get(wine_id)
        if not wine:
            return abort(404, f'Wine with id {wine_id} does not exist')
        try:
            wine.delete()

        except Exception as e:
            print(e)
            return abort(500)

        return jsonify({
            'success': True,
            'deleted': wine.format()
        })

    @app.route('/districts/<int:district_id>', methods=['DELETE'])
    @requires_auth('delete:districts')
    def delete_district(payload, district_id):
        district = District.query.get(district_id)

        if not district:
            return abort(404, f'District with id {district_id} does not exist')

        try:
            district.delete()

        except Exception as e:
            print(e)
            return abort(500)

        return jsonify({
            'success': True,
            'deleted': district.format()
        })

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

        try:
            wine.update()

        except Exception as e:
            print(e)
            return abort(422)

        return jsonify({
            'success': True,
            'Wine': wine.format()
        })

    @app.route('/districts/<int:district_id>', methods=['PATCH'])
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

        try:
            district.update()

        except Exception as e:
            print(e)
            return abort(422)

        return jsonify({
            'success': True,
            'district': district.format()
        })

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

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": error.description
        }), 500

    @app.errorhandler(AuthError)
    def handle_auth_error(exception):
        response = jsonify(exception.error)
        response.status_code = exception.status_code
        return response

    return app


app = create_app()
