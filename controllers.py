	
from flask.views import MethodView
from flask import Flask
from flask import jsonify, request
import time
from flask_mysqldb import MySQL
import bcrypt
import jwt
from config import KEY_TOKEN_AUTH
import datetime
from model import users

#configurar de la app
app = Flask(__name__)
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="1234"
app.config["MYSQL_DB"]="restaurante"
mysql=MySQL(app)
app.secret_key='mysecretKey'
class LoginUserControllers(MethodView):
    """
        Example Login
    """
    def post(self):
        #donde almacenan los datos de la base de datos
        datos = ""
        #simulacion de espera en el back con 1.5 segundos
        time.sleep(3)
        #config de json
        content = request.get_json()
        #traigo el objeto
        correo = content.get("email")
        password = content.get("password")
        cur=mysql.connection.cursor()
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"
        cur.execute("""select nombre,apellido,email,administrador,clave from usuarios where email = %s""",([correo]))
        datos = cur.fetchall()
        datos = datos[0]
        print(datos[2])
        #se pasan los atributos al email y clave
        email = datos[2]
        clave = datos[4]
        admin = datos[3]
        print(datos[3])
        #GUARDAR EN UN DICCIONARIO LOS DATOS EMAIL Y CLAVE
        users[email] = {"contraseña":clave}
        #VERIFICAR SI CORREO ES IGUAL AL EMAIL
        if users.get(correo):
            #print("fuciona")
            #LLAMAMOS AL DATOS EMAIL CON CORREO PARA NOS RETORNE LA CLAVE
            contrasenaUser= users[correo]["contraseña"]
            #print("CONTRASEÑA USUARIO ",contrasenaUser)
            if bcrypt.checkpw(bytes(str(password), encoding='utf-8'),contrasenaUser.encode('utf-8')):
                encoded_jwt = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=600), 'email': email,'admin': admin}, KEY_TOKEN_AUTH , algorithm='HS256')
                #return print("EXITOSO")
                return jsonify({"Status": "Login exitoso","token": encoded_jwt,"name":datos[1]}), 200
            else:
                return jsonify({"Status": "Login incorrecto 22"}), 400
        else:    
            return jsonify({"auth": False}), 400
class RegisterUserControllers(MethodView):
    def post(self):
        time.sleep(3)
        content = request.get_json()
        email = content.get("email")
        name = content.get("name")
        password = content.get("password")
        lastname = content.get("lastname")
        print(password)
        #se acripta el password, se obtiene el hash
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(bytes(str(password), encoding= 'utf-8'), salt)
        print("ENCRIPTADA: ",hash_password)
        cur=mysql.connection.cursor()
        cur.execute("""
        insert into usuarios
        (nombre,apellido,email,clave)
        values
        (%s,%s,%s,%s);
        """,(name,lastname,email,hash_password))
        mysql.connection.commit()
        cur.close()
        return jsonify({"Register ok": True}),200
class Productos(MethodView):
    def get(self):
        cur=mysql.connection.cursor()
        cur.execute('SELECT * FROM productos')
        datos = cur.fetchall()
        payload = []
        content = {}
        for result in datos:
            content = {'id':result[0],'nombre':result[1],'ulrImg':result[2]}
            payload.append(content)
            content = {}
        return jsonify({"datos": payload}),200
class PedidosUserControllers(MethodView):
    def get(self):
        if (request.headers.get('Authorization')):
            token = request.headers.get('Authorization').split(" ")
            print("-----------------_", token[1])
            try:
                payload = []
                data = jwt.decode(token[1], KEY_TOKEN_AUTH , algorithms=['HS256'])
                info = {'correo':data.get("email"),'admin':data.get("admin")}
                payload.append(info)
                return jsonify({"datos": payload}), 200
            except:
                return jsonify({"Status": "TOKEN NO VALIDO"}), 403
        return jsonify({"Status": "No ha enviado un token"}), 403
class ReservarUserControllers(MethodView):
    def post(self):
        try:
            content = request.get_json() 
            cel=content.get("cel")
            fecha=content.get("fecha")
            personas=content.get("personas")
            idusuario=content.get("idusuario")
            #genera un objeto cursor
            cur= mysql.connection.cursor()
            
            #ejecutar comandos de MySQL
            cur.execute("INSERT INTO  reservacion(cel,fecha,personas,idusuario) VALUES(%s,%s,%s,%s)",(cel,fecha,personas,idusuario))
            #actualiza la informacion que acaba de ingresar 
            mysql.connection.commit()
            #cerrar la conecion
            cur.close()
            return jsonify({"data":True}),200
        except:
            return "Lo sentimos el registro ya se ha hecho antes "
class ProductosId(MethodView):
    def post(self):
        content = request.get_json()
        id = content.get("id")
        cur=mysql.connection.cursor()
        cur.execute('SELECT titulo,urlImg,precio FROM `productos` WHERE id = %s;',([id]))
        datos=cur.fetchall()
        payload = []
        for result in datos:
            content = {'nombre':result[0],'ulrImg':result[1],'precio':result[2]}
            payload.append(content)
            content = {}
        return jsonify({"datos": payload}),200


class PedidosUser(MethodView):
    def post(self):
        time.sleep(3)
        content = request.get_json()
        direccion = content.get('direccion')
        numeroS = content.get('numeroSecundario')
        fecha = content.get('fecha')
        cantidad = content.get('cantidad')
        comida = content.get('comida')
        usuario = content.get('user')
        try:
            cur=mysql.connection.cursor()
            cur.execute("""
            insert into pedidos
            (direccion,numeroSecudario,cantidad,producto,correo,fecha)
            values
            (%s,%s,%s,%s,%s,%s);
            """,(direccion,numeroS,cantidad,comida,usuario,fecha))
            mysql.connection.commit()
            cur.close()
            return jsonify({"datos": True}),200
        except:
            return jsonify({"datos": False}),403

class updateProduct(MethodView):
    def post(self):
        time.sleep(3)
        content = request.get_json()
        id = content.get('id')
        nombre = content.get('nombre')
        urlImg =  content.get('ulrImg')
        precio =  content.get('precio')
        try:
            cur = mysql.connection.cursor()
            cur.execute(
            """
            UPDATE productos
            SET titulo = %s, urlImg= %s,precio = %s
            WHERE id = %s;
            """,([nombre,urlImg,precio,id]))
            mysql.connection.commit()
            cur.close
            return jsonify({"datos": True}),200
        except:
            return jsonify({"datos":False}),403
class delete(MethodView):
    def post(self):
        time.sleep(1)
        content = request.get_json()
        id = content.get('id')
        try:
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM productos WHERE id = %s",([id]))
            mysql.connection.commit()
            cur.close()
            return jsonify({"datos": True}),200
        except:
            return jsonify({"datos": False}),403

class agregar(MethodView):
    def post(self):
        time.sleep(1)
        content = request.get_json()
        nombre = content.get('nombre')
        precio = content.get('precio')
        url = content.get('urlImg')
        try:
            cur=mysql.connection.cursor()
            cur.execute("""
            insert into productos
            (titulo,urlImg,precio)
            values
            (%s,%s,%s);
            """,(nombre,url,precio))
            mysql.connection.commit()
            cur.close()
            return jsonify({"datos": True}),200
        except:
            return jsonify({"datos": False}),403
        