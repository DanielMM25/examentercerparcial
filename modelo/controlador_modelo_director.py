from flask import jsonify, request
from .conectar import conexion

def buscar_director(codigo):
    try:
        conn = conexion()
        cur = conn.cursor()
        cur.execute("SELECT nombre, pais_nacimiento, fecha_nacimiento, cant_peliculas_dirigidas FROM directores WHERE nombre = %s", (codigo,))
        datos = cur.fetchone()
        conn.close()
        if datos:
            director = {
                'nombre': datos[0],
                'pais_nacimiento': datos[1],
                'fecha_nacimiento': datos[2].strftime('%Y-%m-%d'),
                'cant_peliculas_dirigidas': datos[3]
            }
            return director
        else:
            return {}
    except Exception as ex:
        raise ex

class DirectorModel():
    @classmethod
    def listar_directores(cls):
        try:
            conn = conexion()
            cur = conn.cursor()
            cur.execute("SELECT nombre, pais_nacimiento, fecha_nacimiento, cant_peliculas_dirigidas FROM directores")
            datos = cur.fetchall()
            directores = []
            for fila in datos:
                director = {
                    'nombre': fila[0],
                    'pais_nacimiento': fila[1],
                    'fecha_nacimiento': fila[2].strftime('%Y-%m-%d'),
                    'cant_peliculas_dirigidas': fila[3]
                }
                directores.append(director)
            conn.close()
            return jsonify({'directores': directores, 'mensaje': "Lista de Directores.", 'exito': True})
        except Exception as ex:
            return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})

    @classmethod
    def registrar_director(cls):
        try:
            director = buscar_director(request.json['nombre'])
            if director:
                return jsonify({'mensaje': "El director ya existe, no se puede duplicar.", 'exito': False})
            else:
                conn = conexion()
                cur = conn.cursor()
                cur.execute('INSERT INTO directores VALUES (%s,%s,%s,%s)',
                            (request.json['nombre'], request.json['pais_nacimiento'], request.json['fecha_nacimiento'],
                             request.json['cant_peliculas_dirigidas']))
                conn.commit()
                conn.close()
                return jsonify({'mensaje': "Director registrado.", 'exito': True})
        except Exception as ex:
            return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})

    @classmethod
    def eliminar_director(cls, codigo):
        try:
            director = buscar_director(codigo)
            if director:
                conn = conexion()
                cur = conn.cursor()
                cur.execute("DELETE FROM directores WHERE nombre = %s", (codigo,))
                conn.commit()
                conn.close()
                return jsonify({'mensaje': "Director eliminado.", 'exito': True})
            else:
                return jsonify({'mensaje': "Director no encontrado.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})

    @classmethod
    def actualizar_director(cls, codigo):
        try:
            director = buscar_director(codigo)
            if director:
                conn = conexion()
                cur = conn.cursor()
                cur.execute("""UPDATE directores SET pais_nacimiento=%s, fecha_nacimiento=%s,
                            cant_peliculas_dirigidas=%s WHERE nombre=%s""",
                            (request.json['pais_nacimiento'], request.json['fecha_nacimiento'],
                             request.json['cant_peliculas_dirigidas'], codigo))
                conn.commit()
                conn.close()
                return jsonify({'mensaje': "Director actualizado.", 'exito': True})
            else:
                return jsonify({'mensaje': "Director no encontrado.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})
