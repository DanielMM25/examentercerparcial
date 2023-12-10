from flask import Flask,request,jsonify
from decouple import config
from flask_cors import CORS
from modelo.controlador_modelopelicula import PeliculaModel
from modelo.controlador_modelo_director import DirectorModel
from modelo.controlador_modelo_actor import ActorModel

app = Flask(__name__)	
CORS(app,resources={r"/actores/*": {"origins": "https://tercer-parcial.onrender.com/"}},
)
CORS(app,resources={r"/peliculas/*": {"origins": "https://tercer-parcial.onrender.com/"}},
)
CORS(app,resources={r"/directores/*": {"origins": "https://tercer-parcial.onrender.com/"}},
)

@app.route('/peliculas', methods=['GET'])
def listar_peliculas():
    x=PeliculaModel.listar_pelicula()
    return x
@app.route('/peliculas', methods=['POST'])
def registrar_peliculas():
    x=PeliculaModel.registrar_pelicula()
    return x
@app.route('/peliculas/:<codigo>', methods=['DELETE'])
def eliminar_peliculas(codigo):
    x= PeliculaModel.eliminar_pelicula(codigo)
    return x
@app.route('/peliculas/:<codigo>', methods=['PUT'])
def actualizar_peliculas(codigo):
    x= PeliculaModel.actualizar_pelicula(codigo)
    return x

@app.route('/directores', methods=['GET'])
def listar_directores():
    x = DirectorModel.listar_directores()
    return x
@app.route('/directores', methods=['POST'])
def registrar_directores():
    x = DirectorModel.registrar_director()
    return x
@app.route('/directores/:<codigo>', methods=['DELETE'])
def eliminar_directores(codigo):
    x = DirectorModel.eliminar_director(codigo)
    return x
@app.route('/directores/:<codigo>', methods=['PUT'])
def actualizar_directores(codigo):
    x = DirectorModel.actualizar_director(codigo)
    return x
@app.route('/actores', methods=['GET'])
def listar_actores():
    x = ActorModel.listar_actores()
    return x
@app.route('/actores', methods=['POST'])
def registrar_actores():
    x = ActorModel.registrar_actor()
    return x
@app.route('/actores/<nombre>', methods=['DELETE'])
def eliminar_actores(nombre):
    x = ActorModel.eliminar_actor(nombre)
    return x
@app.route('/actores/<nombre>', methods=['PUT'])
def actualizar_actores(nombre):
    x = ActorModel.actualizar_actor(nombre)
    return x

if __name__ == '__main__':
   
    app.run(debug=True,host='0.0.0.0')
