from flask import jsonify, request
from .conectar import conexion

def buscar_actor(nombre):
    try:
        conn = conexion()
        cur = conn.cursor()
        cur.execute("SELECT nombre, pais_nacimiento, fecha_nacimiento, genero_preferido, estatura FROM actores WHERE nombre = %s", (nombre,))
        datos = cur.fetchone()
        conn.close()
        if datos:
            actor = {
                'nombre': datos[0],
                'pais_nacimiento': datos[1],
                'fecha_nacimiento': datos[2],
                'genero_preferido': datos[3],
                'estatura': datos[4]
            }
            return actor
        else:
            return {}
    except Exception as ex:
        raise ex

class ActorModel():
    @classmethod
    def listar_actores(cls):
        try:
            conn = conexion()
            cur = conn.cursor()
            cur.execute("SELECT nombre, pais_nacimiento, fecha_nacimiento, genero_preferido, estatura FROM actores")
            datos = cur.fetchall()
            actores = []
            for fila in datos:
                actor = {
                    'nombre': fila[0],
                    'pais_nacimiento': fila[1],
                    'fecha_nacimiento': fila[2],
                    'genero_preferido': fila[3],
                    'estatura': fila[4]
                }
                actores.append(actor)
            conn.close()
            return jsonify({'actores': actores, 'mensaje': "Lista de Actores.", 'exito': True})
        except Exception as ex:
            return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})

    @classmethod
    def registrar_actor(cls):
        try:
            actor = buscar_actor(request.json['nombre'])
            if actor:
                return jsonify({'mensaje': "Nombre de actor ya existe, no se puede duplicar.", 'exito': False})
            else:
                conn = conexion()
                cur = conn.cursor()
                cur.execute('INSERT INTO actores VALUES (%s,%s,%s,%s,%s)',
                            (request.json['nombre'], request.json['pais_nacimiento'], request.json['fecha_nacimiento'],
                             request.json['genero_preferido'], request.json['estatura']))
                conn.commit()
                conn.close()
                return jsonify({'mensaje': "Actor registrado.", 'exito': True})
        except Exception as ex:
            return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})

    @classmethod
    def eliminar_actor(cls, nombre):
        try:
            actor = buscar_actor(nombre)
            if actor:
                conn = conexion()
                cur = conn.cursor()
                cur.execute("DELETE FROM actores WHERE nombre = %s", (nombre,))
                conn.commit()
                conn.close()
                return jsonify({'mensaje': "Actor Eliminado.", 'exito': True})
            else:
                return jsonify({'mensaje': "Actor no Encontrado.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})

    @classmethod
    def actualizar_actor(cls, nombre):
        try:
            actor = buscar_actor(nombre)
            if actor:
                conn = conexion()
                cur = conn.cursor()
                cur.execute("""UPDATE actores SET pais_nacimiento=%s, fecha_nacimiento=%s,
                            genero_preferido=%s, estatura=%s WHERE nombre=%s""",
                            (request.json['pais_nacimiento'], request.json['fecha_nacimiento'],
                             request.json['genero_preferido'], request.json['estatura'], nombre))
                conn.commit()
                conn.close()
                return jsonify({'mensaje': "Actor actualizado.", 'exito': True})
            else:
                return jsonify({'mensaje': "Actor no encontrado.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})
