import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from urllib.request import urlopen

from app import create_app
from models.models import setup_db, Wine, District



class WineApiTestCase(unittest.TestCase):
    

    def setUp(self):
        
        self.app = create_app()
        self.client = self.app.test_client
        self.subscriber_token = os.environ.get('WINE_SUBSCRIBER_TOKEN')
        self.editor_token = os.environ.get('WINE_EDITOR_TOKEN')
        self.postgres_user = os.environ.get('POSTGRESQL_USER')
        self.database_name = os.environ.get('TEST_DATABASE')
        self.database_path = "postgresql://{}@{}/{}".format(self.postgres_user,'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        load_dotenv()

        self.new_wine = {
            'producer': 'Scarpa',
            'vintage': '2010',
            'grape': 'Barbera',
            'vinyard': "I'bricchi",
            'rating': '89',
            'district_id': '2'
        }
        self.new_wine_incomplete_data = {
            'producer': 'Scarpa',
            'vinyard': "La Bogliona",
            'rating': 89,
            'district_id': '2'
        }

        self.new_district = {
            'name': 'Montefalco',
            'province': 'Piemonte'
        }

        self.new_district_incomplete_data = {
            'name': 'Montestefano'
        }

        self.subscriber_header = {"Authorization":f'Bearer {self.subscriber_token}'}

        self.editor_header = {"Authorization":f'Bearer {self.editor_token}'}

        
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            # self.db.create_all()
        



    def tearDown(self):
        
        pass

    
    def test_index_health(self):
        res = self.client().get('/')
        
        self.assertEqual(res.status_code, 200)


    def test_get_wines_unauthorized(self):
        res = self.client().get('/wines')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], 'Not authorized')


    def test_get_wines_authorized(self):


        res = self.client().get('/wines', headers=self.subscriber_header,)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)


    def test_get_wines_paginated_authorized(self):


        res = self.client().get('/wines?page=1', headers=self.subscriber_header,)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)


    def test_fail_get_wines_paginated_out_of_bounds_authorized(self):


        res = self.client().get('/wines?page=100', headers=self.editor_header,)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)    


    def test_get_wine_by_id_authorized(self):
        res = self.client().get('/wines/1', headers=self.editor_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_fail_get_wine_by_id_out_of_bounds(self):
        res = self.client().get('/wines/1000', headers=self.editor_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        


    def test_get_districts_unauthorized(self):
        res = self.client().get('/districts')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], 'Not authorized')


    def test_get_districts_authorized(self):
        res = self.client().get('/wines', headers=self.editor_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_get_wines_by_district(self):
        res = self.client().get('/districts/1', headers=self.editor_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_fail_get_wines_by_out_of_bounds_district(self):
        res = self.client().get('/districts/1000', headers=self.editor_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
    
    def test_insert_district_authorized(self):
        res = self.client().post('/districts', headers=self.editor_header, json=self.new_district)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['created'], True)
    

    def test_insert_district_unauthorized(self):
        res = self.client().post('/districts', headers=self.subscriber_header, json=self.new_district)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)


    def test_insert_district_incomplete_data(self):
        res = self.client().post('/districts', headers=self.editor_header, json=self.new_district_incomplete_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    
    def test_insert_wine_authorized(self):

        res = self.client().post('/wines', headers=self.editor_header, json=self.new_wine)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_insert_wine_unauthorized(self):

        res = self.client().post('/wines', headers=self.subscriber_header, json=self.new_wine)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)    

    
    def test_fail_insert_wine_incomplete_data(self):

        res = self.client().post('/wines', headers=self.editor_header, json=self.new_wine_incomplete_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)


    def test_delete_wine_authorized(self):

        #Creates a new instance of a wine object so it never deletes an actual database instance

        wine = Wine(**self.new_wine)
        wine.insert()
        id_wine = wine.id
        res = self.client().delete(f'/wines/{id_wine}', headers=self.editor_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['deleted'], True)


    def test_delete_wine_unauthorzied(self):
        res = self.client().delete('/wines/1', headers=self.subscriber_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)


    def test_fail_delete_wine_out_of_bounds(self):
        res = self.client().delete('/wines/2000', headers=self.editor_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'], False)

    
    def test_delete_district_authorized(self):

        district = District(**self.new_district)
        district.insert()
        id_district = district.id

        res = self.client().delete(f'/districts/{id_district}', headers=self.editor_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['deleted'], True)
    

    def test_delete_district_unauthorized(self):

        res = self.client().delete(f'/districts/1', headers=self.subscriber_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_fail_delete_district_out_of_bounds(self):

        res = self.client().delete('/districts/2000', headers=self.editor_header)
        data = json.loads(res.data)
    
    def test_edit_district_authorized(self):

        res = self.client().patch('/districts/30', headers=self.editor_header, json={"name":"Soave Classico"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['district'], True)

    def test_edit_district_unauthorized(self):

        res = self.client().patch('/districts/30', headers=self.subscriber_header, json={"name":"Soave Imana"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_fail_edit_district_out_of_bounds(self):

        res = self.client().patch('/districts/2000', headers=self.editor_header, json={"name":"Soave Imana"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


    def test_edit_wine_authorized(self):

        res = self.client().patch('/wines/5', headers =self.editor_header, json={"rating":"75"})
        data = json.loads(res.data)
    
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['Wine']['rating'], 75)
    
    def test_edit_wine_unauthorized(self):

        res = self.client().patch('/wines/5', headers =self.subscriber_header, json={"rating":"85"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_edit_wine_out_of_bounds(self):

        res = self.client().patch('/wines/2000', headers =self.editor_header, json={"rating":"75"})
        data = json.loads(res.data)
    
        self.assertEqual(res.status_code,404)
        self.assertFalse(data['Wine']['rating'], True)


    #OMG THAT'S A LOT OF TESTS


if __name__ == "__main__":
        unittest.main() 