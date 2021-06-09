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
    negocio  = request.form.get('nombreEmpresa')
    print(negocio)
    try:
      os.mkdir('imagenes/logo/')
      print("negocio: ", negocio)
      f.save(os.path.join("imagenes/logo/",secure_filename(negocio+"_imagen.png")))
      img = negocio+"_imagen.png"
      return jsonify({"img": img})
    except FileExistsError:
      f.save(os.path.join("imagenes/logo/",secure_filename(negocio+"_imagen.png")))
      img = negocio+"_imagen.png"
      return jsonify({"img": img})



@app.route('/imagenes/<string:name>')
def get_images(name):
    return (send_from_directory(os.getcwd()+"/imagenes/logo/",name))


if __name__ == '__main__':
   app.run(debug = True,port= 8000,host='0.0.0.0')
