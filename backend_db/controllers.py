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
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_DB"]="bd_click"
mysql=MySQL(app)
app.secret_key='mysecretKey'


class Pedido(MethodView):
    def post(self):
        #time.sleep(3)
        content = request.get_json()
        nombres = content.get("nombres")
        apellidos = content.get("apellidos")
        telefono = content.get("telefono")
        correo = content.get("correo")
        direccion = content.get("direccion")        
        cursor = mysql.connection.cursor()
        cursor.execute("""INSERT INTO comprador (nombres, apellidos, telefono, correo, direccion) VALUES(%s, %s, %s, %s, %s)""",(nombres, apellidos, telefono, correo, direccion))
        mysql.connection.commit()
        cursor.close
        return jsonify({"Se ha registrado el pedido": True, "nombres": nombres, "apellidos": apellidos, "telefono": telefono, "correo": correo, "direccion": direccion})

class LoginUserControllers(MethodView):
    """
        Example Login
    """
    def post(self):
        #donde almacenan los datos de la base de datos
        datos = ""
        #simulacion de espera en el back con 1.5 segundos
        #config de json
        content = request.get_json()
        #traigo el objeto
        correo = content.get("email")
        password = content.get("password")
        cur=mysql.connection.cursor()
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"
        cur.execute("""SELECT * FROM usuario 
        WHERE correo = %s;""",([correo]))

        datos = cur.fetchall()
        print("DATOS DE LA BASE DE DATOS: ",datos)
        datos = datos[0]
        print("ESTE ES CORREO DE LA BD: ",datos[1])
        #se pasan los atributos al email y clave
        email = datos[1]
        clave = datos[8]
        admin = datos[3]
        print("ESTA LA CONTRASEÑA DE LA BD: ",datos[8])
        #trim()
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
                encoded_jwt = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=600), 'email': email}, KEY_TOKEN_AUTH , algorithm='HS256')
                #return print("EXITOSO")
                return jsonify({"status": "Login exitoso", "id_usuario":datos[0], "correo":datos[1], "nombres":datos[2], "apellidos":datos[3], "tipo_documento":datos[4], "numero_documento":datos[5], "fecha_nacimiento":datos[6], "numero_telefono":datos[7], "token": encoded_jwt('utf-8')}), 200
            else:
                return jsonify({"status": "Usuario y contraseña no validos"}), 400
        else:    
            return jsonify({"auth": False}), 400

class DatosEmpresa(MethodView):
    def get(self):
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, nombrenegocio, tipo, direccion, horarios, telefono1, telefono2, correo, idusuario, logo FROM negocio;")
        negocios = cur.fetchall()
        cur.close()
        datos = []
        content = {}
        for valor in negocios:
            content = {'id':valor[0], 'nombre':valor[1], 'tipo':valor[2], 'direccion':valor[3], 'horarios':valor[4], 'telefono1':valor[5], 'telefono2':valor[6], 'correo':valor[7], 'id_usuario':valor[8], 'imgLogo':valor[9]}
            datos.append(content)
            content = {}
        #print("DATOS DEL NEGOCIO: ",datos)

        return jsonify({"ok":True, "data": datos}),200
class DatosEmpresaId(MethodView):
    def post(self):
        content = request.get_json()
        id = content.get("id")
        print("ID DEL FRONT:",id)
        return jsonify({'data':id})
    def get(self):
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, nombrenegocio, tipo, direccion, horarios, telefono1, telefono2, correo, idempresario, logo FROM negocio WHERE id = 1;")
        negocio = cur.fetchall()
        cur.close()
        datos = []
        content = {}
        for valor in negocio:
             content = {'id':valor[0], 'nombre':valor[1], 'tipo':valor[2], 'direccion':valor[3], 'horarios':valor[4], 'telefono1':valor[5], 'telefono2':valor[6], 'correo':valor[7], 'id_cliente':valor[8], 'imgLogo':valor[9]}
             datos.append(content)
             content = {}
        cur.close()
        return jsonify({"ok":True, "data":datos}),200


class ProductosEmpresa(MethodView):
    def get(self):
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, foto, nombre, precio, idnegocio, descripcion, iva FROM producto WHERE idnegocio=1;")
        productos = cur.fetchall()
        cur.close()
        datos = []

        content = {}
        for valor in productos: 
            content = {'id':valor[0], 'foto':valor[1], 'nombre':valor[2], 'precio':valor[3], 'idnegocio':valor[4], 'descripcion':valor[5], 'iva':valor[6]}
            datos.append(content)
            content = {}
        #print("DATO0S DE PRODUCTOS DESDE LA BD: ", datos)
        
        return jsonify({"ok":True,"data": datos})




class EnviarProductos(MethodView):
    def post(self):
        content = request.get_json()
        data = content.get("data")
        cur=mysql.connection.cursor()
        print("DATOS DEL FRONTEND:",data)
        cur.execute('SELECT id, foto, nombre, precio, idnegocio, descripcion FROM producto WHERE idnegocio = 1 AND id = %s',([id]))
        datos = cur.fetchall()
        cur.close()
        #print("DATOS: ",datos)
        payload = []
        content = {}
        for result in datos:
            content = {'id':result[0], 'foto':result[1], 'nombre':result[2], 'precio':result[3],'id_negocio':result[4], 'descripcion':result[5]}
            payload.append(content)
            content = {}
        #print("DATOS DE PRODUCTOS POR ID: ", payload)
        return jsonify({"data": payload}),200

class RegisterUserControllers(MethodView):
    def post(self):
        content = request.get_json()
        nombres = content.get("nombres")
        apellidos = content.get("apellidos")
        tipoDocumento = content.get("tipoDocumento")
        numDocumento = content.get("numeroDocumento")
        numeroTel = content.get("numeroTelefono")
        fechaNacimiento = content.get("fechaNacimiento")
        correo = content.get("email")
        password = content.get("password")
        
        print(password)
        #se acripta el password, se obtiene el hash
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(bytes(str(password), encoding= 'utf-8'), salt)
        print("ENCRIPTADA: ",hash_password)
        cur=mysql.connection.cursor()
        cur.execute("""INSERT INTO usuario
        (correo, nombres, apellidos, tipodoc, 
        numerodoc, numtelefono, fechanac, pass)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s);
        """,(correo, nombres, apellidos, tipoDocumento, numDocumento, numeroTel, fechaNacimiento,  hash_password))
        if (correo):
            #mysql.connection.commit()
            print("mysql.connection.commit(): ", mysql.connection.commit() )
            #cur.close()
            return jsonify({"Registro ok": True, "Nombres":nombres, "Apellidos":apellidos, "Tipo Documemto":tipoDocumento, "Numero de documento":numDocumento, "Numero Telefono":numeroTel, "Fecha Nacimiento":fechaNacimiento, "Correo":correo,   }),200
        else:
            return jsonify({"status":"El correo ya existe"}), 403

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

#MODULO NEGOCIO

#Mostrar negocios
class MostrarTodosLosNegocios(MethodView):
    def get(self):

        cur = mysql.connection.cursor()
        cur.execute("SELECT id, nombrenegocio, tipo, direccion, horarios, telefono1, telefono2, correo, idusuario, logo FROM negocio;")
        negocios = cur.fetchall()
        cur.close()
        datos = []
        content = {}
        for valor in negocios:
            content = {'id':valor[0], 'nombre':valor[1], 'tipo':valor[2], 'direccion':valor[3], 'horarios':valor[4], 'telefono1':valor[5], 'telefono2':valor[6], 'correo':valor[7], 'id_usuario':valor[8], 'logo':valor[9]}
            datos.append(content)
            content = {}
        return jsonify({"data": datos}),200

class MostrarNegocios(MethodView):
    def get(self):
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, nombrenegocio, tipo, direccion, horarios, telefono1, telefono2, correo, idusuario, logo FROM negocio WHERE idusuario = 1;")
        negocios = cur.fetchall()
        cur.close()
        datos = []
        content = {}
        for valor in negocios:
            content = {'id':valor[0], 'nombre':valor[1], 'tipo':valor[2], 'direccion':valor[3], 'horarios':valor[4], 'telefono1':valor[5], 'telefono2':valor[6], 'correo':valor[7], 'id_usuario':valor[8], 'imgLogo':valor[9]}
            datos.append(content)
            content = {}
        return jsonify({"Datos de los negocios":True, "Datos": datos}),200

class MostrarNegocio(MethodView):
    def get(self):
        id_negocio = request.args.get('id')
        print(id_negocio)
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, nombrenegocio, tipo, direccion, horarios, telefono1, telefono2, correo, logo FROM negocio WHERE id = %s;",([id_negocio]))
        negocio = cur.fetchall()
        cur.close()
        datos = []
        content = {}
        for valor in negocio:
            content = {'id':valor[0], 'nombre':valor[1], 'tipo':valor[2], 'direccion':valor[3], 'horarios':valor[4], 'telefono1':valor[5], 'telefono2':valor[6], 'correo':valor[7], 'logo':valor[8]}
            datos.append(content)
            content = {}
        return jsonify({"Datos del negocio": True, "data": datos}),200

class MostrarNegocioId(MethodView):
    def get(self):
        id_negocio = request.args.get('id')
        print(id_negocio)
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, nombrenegocio, tipo, direccion, horarios, telefono1, telefono2, correo, logo FROM negocio WHERE idusuario = 1 AND id = %s;",([id_negocio]))
        negocio = cur.fetchall()
        cur.close()
        datos = []
        content = {}
        for valor in negocio:
            content = {'id':valor[0], 'nombre':valor[1], 'tipo':valor[2], 'direccion':valor[3], 'horarios':valor[4], 'telefono1':valor[5], 'telefono2':valor[6], 'correo':valor[7], 'logo':valor[8]}
            datos.append(content)
            content = {}
        return jsonify({"Datos del negocio": True, "data": datos}),200

#Clase de registro de la empresa
class RegisterEmpresaControllers(MethodView):
    def post(self):
        content = request.get_json()
        nombre = content.get("nombre")
        tipoE = content.get("tipoE")
        direccionE = content.get("direccionE")
        numeroE = content.get("numeroE")
        numeroS = content.get("numeroS")
        emailE = content.get("emailE")
        #Este id esta ya predeterminado 
        id_usuario = 1
        #Horario de la empresa 
        horario = content.get("horario")
        logo = content.get("logo")
        cur=mysql.connection.cursor()
        cur.execute("""
        insert into negocio(nombrenegocio,tipo,direccion,telefono1,telefono2,correo,idusuario,horarios,logo)
        values
        (%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """,(nombre,tipoE,direccionE,int(numeroE),int(numeroS),emailE,int(id_usuario),horario,logo))
        mysql.connection.commit()
        cur.close()
        return jsonify({"data": True}),200



class ActualizarNegocio(MethodView):
    def post(self):
        #try:
        content = request.get_json()
        id_e = content.get("idn")
        nombre = content.get("nombre")
        tipo_empresa = content.get("tipo")
        direccion = content.get("direccion")
        telefono_principal = content.get("telefono1")
        telefono_secundario = content.get("telefono2")
        horarios = content.get("horarios")
        correo = content.get("correo")
        logo = content.get("logo")
        #id_usuario = content.get("idUsuario")

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE negocio SET nombrenegocio = %s, tipo = %s, direccion = %s, horarios = %s, telefono1 = %s, telefono2 = %s, correo = %s, logo = %s
        WHERE id = %s;""",(nombre, tipo_empresa, direccion, horarios, telefono_principal, telefono_secundario, correo, logo, id_e))
        mysql.connection.commit()
        cur.close()
        return jsonify({"Se ha actualizado correctamente": True}),200

class EliminarNegocio(MethodView):
    def delete(self):
        #try:
        id_negocio = request.args.get('id')
        print(id_negocio)
        cur = mysql.connection.cursor()
        cur.execute("""
        DELETE negocio WHERE id = %s;
        """,([id_negocio]))
        mysql.connection.commit()
        cur.close()
        return jsonify({"data": "Se ha eliminado el negocio exitosamente"}),200

#MODULO DE PRODUCTOS

class MostrarProductosNegocio(MethodView):
    def get(self):
        id_negocio = request.args.get('id')
        print(id_negocio)
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, foto, nombre, precio, descripcion FROM producto WHERE idnegocio = %s;",([id_negocio]))
        productos = cur.fetchall()
        cur.close()
        datos = []
        content = {}
        for valor in productos:
            content = {'id':valor[0], 'foto':valor[1], 'nombre':valor[2], 'precio':valor[3], 'descripcion':valor[4]}
            datos.append(content)
            content = {}
        return jsonify({"Obtener Productos": True, "data": datos}),200

class ProductoId(MethodView):
    def get(self):
        id_producto = request.args.get('id')
        print(id_producto)
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, foto, nombre, precio, descripcion FROM producto WHERE id = %s;",([id_producto]))
        producto = cur.fetchall()
        cur.close()
        datos = []
        content = {}
        for valor in producto:
            content = {'id':valor[0], 'foto':valor[1], 'nombre':valor[2], 'precio':valor[3], 'descripcion':valor[4]}
            datos.append(content)
            content = {}
        return jsonify({"Obtener producto": True, "data": datos}),200
class CrearProducto(MethodView):
    def post(self):
        #try:
        content = request.get_json()
        foto = content.get("logo")
        nombre = content.get("nombre")
        precio = content.get("precio")
        id_negocio = content.get("idnegocio")
        descripcion = content.get("descripcion")
        print(id_negocio)
        print(nombre)
        print(descripcion)
        print(precio)
        cur = mysql.connection.cursor()
        cur.execute("""
        INSERT INTO producto (foto, nombre, precio, idnegocio, descripcion) VALUES (%s, %s, %s, %s, %s);
        """,(foto, nombre, precio, id_negocio, descripcion))
        mysql.connection.commit()
        cur.close()
        return jsonify({"Producto creado exitosamente": True}), 200
        #except:

class ActualizarProducto(MethodView):
    def post(self):
        #try:
        time.sleep(2)
        content = request.get_json()
        idproducto = content.get("idProducto")
        foto = content.get("logo")
        nombre = content.get("nombre")
        precio = content.get("precio")
        #idnegocio = content.get("idnegocio")
        descripcion = content.get("descripcion")

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE producto SET foto = %s, nombre = %s, precio = %s, descripcion = %s WHERE id = %s;
        """,(foto, nombre, precio, descripcion, idproducto))
        mysql.connection.commit()
        cur.close()
        return jsonify({"Datos del producto actualizados exitosamente": True}), 200
        #except:


class EliminarProducto(MethodView):
    def post(self):
    #try:
        time.sleep(2)
        id_producto = request.args.get('id')
        print(id_producto)
        cur =mysql.connection.cursor()
        cur.execute("""
        DELETE producto WHERE id = %s;
        """,([id_producto]))
        mysql.connection.commit()
        cur.close()
        return jsonify({"Se ha eliminado el producto exitosamente": True}), 200
    #except: