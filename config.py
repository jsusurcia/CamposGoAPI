import os
from dotenv import load_dotenv

# Obtener la ruta del directorio donde se encuentra este archivo (config.py)
basedir = os.path.abspath(os.path.dirname(__file__))

# Cargar las variables de entorno desde un archivo .env (si existe)
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = int(os.environ.get('DB_PORT', 4000))
    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_DATABASE = os.environ.get('DB_DATABASE')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    ssl_ca = os.path.join(basedir, 'isrgrootx1.pem')
    ssl_verify_cert = True