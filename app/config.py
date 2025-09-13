import os
from dotenv import load_dotenv

load_dotenv()

# Get the base directory of the project
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- For SQLite (a simple file-based database) ---
    # The database will be created in a folder called 'instance' at the root of your project.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, '..', 'instance', 'kizuna.db')
    
    DB_USER = os.environ.get('POSTGRESQL_USERNAME')
    DB_PASSWORD = os.environ.get('POSTGRESQL_PASSWORD')
    DB_HOST = os.environ.get('POSTGRESQL_HOST')
    DB_NAME = os.environ.get('POSTGRESQL_DB_NAME')

    # --- For PostgreSQL (when you're ready to switch) ---
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'