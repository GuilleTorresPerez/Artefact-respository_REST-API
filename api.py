from flask import Flask
from flask_restx import Api, Resource
from flask import send_file

import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './artefacts/'
ALLOWED_EXTENSIONS = {
    "png", "jpg", "jpeg", "gif", "bmp", "svg", "webp",
    "pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "txt", "csv", "md",
    "py", "js", "java", "cpp", "c", "cs", "html", "css", "ts", "json", "xml", "yaml", "yml",
    "zip", "rar", "tar", "gz", "7z",
    "mp4", "mp3", "wav", "flac", "ogg", "avi", "mkv",
}

app = Flask(__name__) # Se inicializa la aplicación Flask con la clase Flask
api = Api(app)  # Se crea una instancia de Api y se asocia a la aplicación Flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def createDirectory(directory):
    try:
        os.makedirs(directory)
    except FileExistsError:
        pass


def upload_file(directory_id, artefact_id):
    if request.method == 'PUT':
        message = {'message': f'File {artefact_id} updated to directory {directory_id}'}
    else: # POST
        message = {'message': f'File {artefact_id} uploaded to directory {directory_id}'}

    if 'file' not in request.files:
        return {'error': 'No file part'}, 400

    file = request.files['file']
    
    if file.filename == '':
        return {'error': 'No file selected'}, 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        createDirectory(app.config['UPLOAD_FOLDER'] + directory_id)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], directory_id, artefact_id))
        return message, 200
        

def delete_directory(directory_id):
    try:
        directory_path = os.path.join(app.config['UPLOAD_FOLDER'], directory_id)
        if os.path.exists(directory_path):
            for root, dirs, files in os.walk(directory_path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(directory_path)
        return {'message': f'Directory {directory_id} deleted and its content'}, 200
    except FileNotFoundError:
        return {'error': 'Directory not found'}, 404

def delete_file(directory_id, artefact_id):
    try:
        artefact_path = os.path.join(app.config['UPLOAD_FOLDER'], directory_id, artefact_id)
        if os.path.exists(artefact_path):
            os.remove(artefact_path)
            return {'message': f'Artefact {artefact_id} deleted from directory {directory_id}'}, 200
        else:
            return {'error': f'Artefact {artefact_id} not found in directory {directory_id}'}, 404
    except FileNotFoundError:
        return {'error': 'Directory not found'}, 404


@api.route('/hello')    # Declara un nuevo endpoint accesible desde http://127.0.0.1:5000/hello
class HelloWorld(Resource): # Define una clase que hereda de Resource, representando los métodos HTTP disponibles para este endpoint.
    def get(self):  # Define un método GET para el endpoint /hello
        return {'hello': 'world'}

@api.route('/artefacts') 
class Artefacts(Resource):
    def get(self):
        try:
            directories = os.listdir(app.config['UPLOAD_FOLDER'])
            return {'directories': directories}, 200  # Devolvemos la lista de directorios
        except FileNotFoundError:
            return {'error': 'Upload folder not found'}, 404

@api.route('/artefacts/<string:directory_id>')
class Artefacts(Resource):
    def get(self, directory_id):
        try:
            directories = os.listdir(app.config['UPLOAD_FOLDER'] + directory_id)
            return {'artefacts': directories}, 200  # Devolvemos la lista de directorios
        except FileNotFoundError:
            return {'error': 'Upload folder not found'}, 404

    def delete(self, directory_id):
        return delete_directory(directory_id)
        

@api.route('/artefacts/<string:directory_id>/<string:artefact_id>')
class Artefacts(Resource):
    def get(self, directory_id, artefact_id):
        artefact_path = os.path.join(app.config['UPLOAD_FOLDER'], directory_id, artefact_id)

        if not os.path.exists(artefact_path):
            return {'error': f'Artefact {artefact_id} not found in directory {directory_id}'}, 404

        try:
            with open(artefact_path, 'rb') as f:
                content = f.read()
            return send_file(artefact_path, as_attachment=True)
        except Exception as e:
            return {'error': f'Failed to read artefact: {str(e)}'}, 500


    def post(self, directory_id, artefact_id):
        return upload_file(directory_id, artefact_id)

    def delete(self, directory_id, artefact_id):
        return delete_file(directory_id, artefact_id)

    def put(self, directory_id, artefact_id):
        return upload_file(directory_id, artefact_id)
            
        

if __name__ == '__main__':
    app.run(debug=True)