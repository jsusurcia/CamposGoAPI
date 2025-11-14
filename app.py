from flask import Flask, jsonify
from conexionBD import Conexion
import pymysql

from routes.routes_usuario import ws_usuario

app = Flask(__name__)
app.register_blueprint(ws_usuario)

@app.route('/')
def home():
    conexion = None
    try:
        # Intentar crear una conexión
        conexion = Conexion()
        
        # Verificar que la conexión esté abierta
        if conexion.open:
            # Hacer una consulta simple para verificar que la BD responda
            conexion.cursor.execute("SELECT 1")
            conexion.cursor.fetchone()
            
            # Cerrar la conexión antes de retornar
            conexion.dblink.close()
            return jsonify({
                "status": "success",
                "message": "Conexión a la base de datos exitosa"
            }), 200
        else:
            if conexion:
                conexion.dblink.close()
            return jsonify({
                "status": "error",
                "message": "La conexión no está abierta"
            }), 500
            
    except pymysql.Error as e:
        # Error específico de MySQL
        if conexion and conexion.open:
            conexion.dblink.close()
        return jsonify({
            "status": "error",
            "message": f"Error de conexión a la base de datos: {str(e)}"
        }), 500
    except Exception as e:
        # Cualquier otro error
        if conexion and conexion.open:
            conexion.dblink.close()
        return jsonify({
            "status": "error",
            "message": f"Error inesperado al conectar: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(debug=True)