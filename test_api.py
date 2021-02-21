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


        res = self.client().get('/wines', headers=self.editor_header,)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)


    def test_get_wines_paginated_authorized(self):


        res = self.client().get('/wines?page=1', headers=self.editor_header,)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)


    def test_fail_get_wines_paginated_out_of_bounds_authorized(self):


        res = self.client().get('/wines?page=100', headers=self.editor_header,)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)    


    def test_get_districts_unauthorized(self):
        res = self.client().get('/districts')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], 'Not authorized')


    def test_get_districts_authorized(self):


        res = self.client().get('/wines', headers=self.editor_header,)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)


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




if __name__ == "__main__":
        unittest.main()