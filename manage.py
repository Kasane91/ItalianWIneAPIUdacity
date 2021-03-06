from flask_script import Manager
from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from dotenv import load_dotenv

from app import app
from models.models import db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
