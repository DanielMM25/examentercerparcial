import pymysql
from decouple import config

def conexion():
    try:
        con = pymysql.connect(
            host=config('HOST'),
            user=config('USUARIO'),
            password=config('CLAVE'),
            db=config('BASE_DATOS')
        )
        return con
    except pymysql.Error as e:
        print(f"Error de conexión a la base de datos: {e}")
        # Puedes decidir cómo manejar el error, como lanzar una excepción o retornar None, según tus necesidades.

