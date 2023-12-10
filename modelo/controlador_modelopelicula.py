from flask import jsonify, request
from .conectar import conexion

def buscar_pelicula(codigo):
    try:
        conn = conexion()
        cur = conn.cursor()
        cur.execute("SELECT titulo, fecha_estreno, genero, duracion, director, protagonista FROM peliculas WHERE titulo = %s", (codigo,))
        datos = cur.fetchone()
        conn.close()
        if datos:
            pelicula = {
                'titulo': datos[0],
                'fecha_estreno': datos[1],
                'genero': datos[2],
                'duracion': datos[3],
                'director': datos[4],
                'protagonista': datos[5]
            }
            return pelicula
        else:
            return {}
    except Exception as ex:
        raise ex

class PeliculaModel():
    @classmethod
    def listar_pelicula(cls):
        try:
            conn = conexion()
            cur = conn.cursor()
            cur.execute("SELECT titulo, fecha_estreno, genero, duracion, director, protagonista FROM peliculas")
            datos = cur.fetchall()
            peliculas = []
            for fila in datos:
                pelicula = {
                    'titulo': fila[0],
                    'fecha_estreno': fila[1],
                    'genero': fila[2],
                    'duracion': fila[3],
                    'director': fila[4],
                    'protagonista': fila[5]
                }
                peliculas.append(pelicula)
            conn.close()
            return jsonify({'peliculas': peliculas, 'mensaje': "Lista de Películas.", 'exito': True})
        except Exception as ex:
            return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})

    @classmethod
    def registrar_pelicula(cls):
        try:
            pelicula = buscar_pelicula(request.json['titulo'])
            if pelicula:
                return jsonify({'mensaje': "La película ya existe, no se puede duplicar.", 'exito': False})
            else:
                conn = conexion()
                cur = conn.cursor()
                cur.execute('INSERT INTO peliculas VALUES (%s,%s,%s,%s,%s,%s)',
                            (request.json['titulo'], request.json['fecha_estreno'], request.json['genero'],
                             request.json['duracion'], request.json['director'], request.json['protagonista']))
                conn.commit()
                conn.close()
                return jsonify({'mensaje': "Película registrada.", 'exito': True})
        except Exception as ex:
            return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})

    @classmethod
    def eliminar_pelicula(cls, codigo):
        try:
            pelicula = buscar_pelicula(codigo)
            if pelicula:
                conn = conexion()
                cur = conn.cursor()
                cur.execute("DELETE FROM peliculas WHERE titulo = %s", (codigo,))
                conn.commit()
                conn.close()
                return jsonify({'mensaje': "Película eliminada.", 'exito': True})
            else:
                return jsonify({'mensaje': "Película no encontrada.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})

    @classmethod
    def actualizar_pelicula(cls, codigo):
        try:
            pelicula = buscar_pelicula(codigo)
            if pelicula:
                conn = conexion()
                cur = conn.cursor()
                cur.execute("""UPDATE peliculas SET fecha_estreno=%s, genero=%s,
                            duracion=%s, director=%s, protagonista=%s WHERE titulo=%s""",
                            (request.json['fecha_estreno'], request.json['genero'],
                             request.json['duracion'], request.json['director'], request.json['protagonista'], codigo))
                conn.commit()
                conn.close()
                return jsonify({'mensaje': "Película actualizada.", 'exito': True})
            else:
                return jsonify({'mensaje': "Película no encontrada.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})
