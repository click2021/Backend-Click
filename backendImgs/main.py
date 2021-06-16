import re
import time
from flask import Flask, request,jsonify,send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/imagenes/<string:name>')
def get_images(name):
    return (send_from_directory(os.getcwd()+"/imagenes/logo/",name,as_attachment=True, cache_timeout=2))


#modulo negocio
@app.route('/deleteImgNegocio', methods=['POST'])
def remove_imageNegocio():
    filename = request.form['filename']
    #VERIFICAMOS SI ES UN FICHERO
    if os.path.isfile(os.getcwd() + "/imagenes/logo/" + filename) == False:
        return jsonify({"status":"es un fichero"})
    else:
        try:
            os.remove(os.getcwd() + "/imagenes/logo/" + filename)
        except OSError:
            return jsonify({"status":"No se elimino el archivo"})
        return jsonify({"status":"Imagen eliminada"})
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
@app.route('/uploadUpgrade', methods = ['POST'])
def upload_update():
  try:
    f = request.files['img']
    nameImg = request.form.get('nameImg')
    print(nameImg)
    f.save(os.path.join("imagenes/logo/",secure_filename(nameImg)))
    return jsonify({"status":True}),200
  except:
    return jsonify({"status":False}),200


#modulo de productos
@app.route('/uploadProducto',methods = ['POST'])
def upload_product():
    f = request.files['img']
    name = request.form.get('name')
    try:
      os.mkdir('imagenes/productos/')
      print("producto: ",name)
      f.save(os.path.join("imagenes/productos/",secure_filename(name+"_imagen.png")))
      img = name+"_imagen.png"
      return jsonify({"img": img})
    except FileExistsError:
      f.save(os.path.join("imagenes/productos/",secure_filename(name+"_imagen.png")))
      img = name+"_imagen.png"
      return jsonify({"img": img})
@app.route('/imagenesProduct/<string:name>')
def get_imagesProduct(name):
    return (send_from_directory(os.getcwd()+"/imagenes/productos/",name,as_attachment=True))

@app.route('/delete', methods=['POST'])
def remove_image():
    filename = request.form['filename']
    #VERIFICAMOS SI ES UN FICHERO
    if os.path.isfile(os.getcwd() + "/imagenes/productos/" + filename) == False:
        return jsonify({"status":"es un fichero"})
    else:
        try:
            os.remove(os.getcwd() + "/imagenes/productos/" + filename)
        except OSError:
            return jsonify({"status":"No se elimino el archivo"})
        return jsonify({"status":"Imagen eliminada"})

@app.route('/uploadProductUpdate', methods = ['POST'])
def upload_updateProduct():
  try:
    f = request.files['img']
    nameImg = request.form.get('name')
    print(nameImg)
    f.save(os.path.join("imagenes/productos/",secure_filename(nameImg)))
    return jsonify({"status":True}),200
  except:
    return jsonify({"status":False}),200

if __name__ == '__main__':
   app.run(debug = True,port= 8000)
