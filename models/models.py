import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, create_engine, Boolean, DateTime, ForeignKey, func, PrimaryKeyConstraint, ForeignKeyConstraint
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from dotenv import load_dotenv
import json 

db = SQLAlchemy()

database_url = os.environ.get('DATABASE_URL', None)
database_name = os.environ.get('DATABASE_NAME')
postgres_user = os.environ.get('POSTGRESQL_USER')

if database_url:
    database_path = database_url
else:
    database_path = "postgresql://{}@{}/{}".format(postgres_user,'localhost:5432', database_name)

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False
    db.app = app
    db.init_app(app)
    
    
def db_drop():
    db.drop_all()

def create_all():
    db.create_all()

class Wine(db.Model):
    __tablename__ = 'wines'

    id = Column(Integer, primary_key=True)
    producer = Column(String(100), nullable=False)
    vintage = Column(Integer, nullable=False)
    grape = Column(String, nullable=False)
    vinyard = Column(String(50))
    rating = Column(Integer)
    district_id = Column(Integer, ForeignKey('districts.id'), nullable=False)

    
    def __init__(self, producer, vintage, grape, vinyard, rating, district_id):
        self.producer = producer
        self.vintage = vintage
        self.grape = grape
        self.vinyard = vinyard
        self.rating = rating
        self.district_id = district_id
    

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def format(self):
        return {
            'id': self.id,
            'producer': self.producer,
            'vintage': self.vintage,
            'grape': self.grape,
            'vinyard': self.vinyard,
            'rating': self.rating,
            'district_id': self.district_id
        }
    

class District(db.Model):
    __tablename__= 'districts'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    province = Column(String(50), nullable=False)
    wines = db.relationship('Wine', backref='district', lazy=True)

    def __init__(self, name, province):
        self.name = name
        self.province = province

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'province' : self.province
        }





