from conexionBD import Conexion
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

class Usuario:
    def __init__(self):
        self.ph = PasswordHasher()


    def obtener_roles(self, usuario_id):
        db = Conexion()
        con = db.dblink
        cursor = db.cursor

        sql = """
            SELECT r.id, r.nombre 
            FROM rol r
            INNER JOIN usuario_rol ur ON ur.rol_id = r.id
            WHERE ur.usuario_id = %s
        """
        cursor.execute(sql, (usuario_id,))
        resultado = cursor.fetchall()
        
        cursor.close()
        con.close()
        
        if resultado:
            return resultado
        return None


    def login(self, email, clave):
        db = Conexion()
        con = db.dblink
        cursor = db.cursor

        sql = """
            SELECT id, concat(nombres, ' ', apellido_paterno, ' ', apellido_materno) AS nombre, email, clave 
            FROM usuario 
            WHERE email = %s
        """

        cursor.execute(sql, [email])
        resultado = cursor.fetchone()

        cursor.close()
        con.close()

        if resultado:
            try:
                hash_almacenado = str(resultado['clave'])
                self.ph.verify(hash_almacenado, clave)
                return resultado
            except VerifyMismatchError:
                return None
        else:
            return None