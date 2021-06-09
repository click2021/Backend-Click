from flask import Flask, request,jsonify,send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route('/upload', methods = ['POST'])
def upload_file():
    f = request.files['img']
    empresa  = request.form.get('nombreEmpresa')
    nombre = empresa.replace("  ","_")
    nombre = empresa.replace(" ","_")
    try:
      os.mkdir('imagenes/'+nombre)
      f.save(os.path.join('imagenes/'+nombre, secure_filename(f.filename)))
      return jsonify({'status':'file uploaded successfully'}),200
    except FileExistsError:
        f.save(os.path.join('imagenes/'+nombre, secure_filename(f.filename)))
        return 'file uploaded successfully'
        

@app.route('/imagenes/<string:filename>, <string:nameEmpresa>')
def get_images(filename, nameEmpresa):
    print("Nombre de la carpeta: ", nameEmpresa.replace(' ','_'))
    print("Nombre del logo: ",filename.replace(' ','_'))
    return send_from_directory(os.getcwd() + "/imagenes/"+nameEmpresa.replace(' ','_')+'/', path=filename.replace(' ','_'), as_attachment=False)


if __name__ == '__main__':
   app.run(debug = True, port= 8000, host='0.0.0.0')