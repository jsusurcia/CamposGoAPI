from flask import Blueprint, request, jsonify, send_from_directory
from models.model_usuario import Usuario
from tools.jwt_utils import generar_token, verificar_token
from tools.jwt_required import jwt_token_requerido
from tools.security import hash_password, password_validate
import os
from datetime import datetime

ws_usuario = Blueprint('ws_usuario', __name__)
usuario = Usuario()

#Endpoint de Login
@ws_usuario.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    clave = data.get('clave')

    #Validar que los datos estén completos
    if not all([email, clave]):
        return jsonify({'status': False, 'data': None, 'message': 'Faltan datos obligatorios'}), 400

    try:
        resultado = usuario.login(email, clave)
        print(resultado)
        if resultado:
            resultado.pop('clave', None)

            #Generar el token en base al ID del usuario, con tiempo de expiración de 60 segundos, y agregarlo al resultado
            token = generar_token({
                "usuario_id": resultado['id'],
            }, 60)
            resultado['token'] = token

            #Obtener los roles del usuario, y agregarlos al resultado
            roles = usuario.obtener_roles(resultado['id'])
            resultado['roles'] = roles

            #Falta: implementar lógica para agregar el ID del vehículo y el token Firebase

            return jsonify({'status': True, 'data': resultado, 'message': 'Login exitoso'}), 200
        else:
            return jsonify({'status': False, 'data': None, 'message': 'Credenciales incorrectas'}), 401
    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500