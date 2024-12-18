from flask import Flask
from flask_restx import Api, Resource

app = Flask(__name__) # Se inicializa la aplicación Flask con la clase Flask
api = Api(app)  # Se crea una instancia de Api y se asocia a la aplicación Flask

@api.route('/hello')    # Declara un nuevo endpoint accesible desde http://127.0.0.1:5000/hello
class HelloWorld(Resource): # Define una clase que hereda de Resource, representando los métodos HTTP disponibles para este endpoint.
    def get(self):  # Define un método GET para el endpoint /hello
        return {'hello': 'world'}

@api.route('/artefacts') 
class Artefacts(Resource):
    def get(self):
        return {'GET_artefacts': 'artefacts'}

# returns list of available directories
@api.route('/artefacts/<string:directory_id>')
class Artefacts(Resource):
    def get(self, directory_id):
        return {'GET_artefacts': directory_id}

    def delete(self, directory_id):
        return {'DELETE_artefacts': directory_id}

# returns list of all artefacts from directory
@api.route('/artefacts/<string:directory_id>/<string:artefact_id>')
class Artefacts(Resource):
    def get(self, directory_id, artefact_id):
        return {'GET_artefacts': directory_id, 'artefact_id': artefact_id}

    def post(self, directory_id, artefact_id):
        return {'POST_artefacts': directory_id, 'artefact_id': artefact_id}

    def delete(self, directory_id, artefact_id):
        return {'DELETE_artefacts': directory_id, 'artefact_id': artefact_id}

    def put(self, directory_id, artefact_id):
        return {'PUT_artefacts': directory_id, 'artefact_id': artefact_id}

if __name__ == '__main__':
    app.run(debug=True)