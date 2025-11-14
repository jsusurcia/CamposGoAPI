import pymysql as dbc
from pymysql.cursors import DictCursor
from config import Config

class Conexion:
    def __init__(self):
        ssl_args = {
            'ca': Config.ssl_ca,
            'verify_cert': Config.ssl_verify_cert
        }
        
        self.dblink = dbc.connect(
            host=Config.DB_HOST,        
            user=Config.DB_USERNAME,        
            password=Config.DB_PASSWORD, 
            database=Config.DB_DATABASE,   
            port=Config.DB_PORT,
            cursorclass=DictCursor,
            ssl=ssl_args
        )
        self.cursor = self.dblink.cursor()

    @property
    def open(self):
        return self.dblink.open