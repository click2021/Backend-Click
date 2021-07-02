from os import truncate
import smtplib
import re
from MySQLdb import DATETIME
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
import json
from datetime import datetime as tiempo
#configurar de la app
app = Flask(__name__)
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_DB"]="bd_click"
mysql=MySQL(app)
app.secret_key='mysecretKey'


#Registrar pedido 
class RegistroPedido(MethodView):
    def post(self):
        content = request.get_json()
        iva = content.get("iva")
        valor = content.get("valorTotal")
        idnegocio = content.get("id_negocio")
        info = content.get("fecha")
        #se cambia el formato de la fecha.
        idusuario = content.get("id_usuario")
        hora = tiempo.now()
        fecha = hora.strftime("%Y-%m-%d %H:%M:%S GTM-0500")
        #print("convertida+convertidaT: ", fechaCovertida)
        print("ESTE ES EL VALOR DEL PEDIDO: ",
       "idnegocio: ", idnegocio,
       "iva: ", iva,
       "valor: ", valor,
       "fechaCovertida:", fecha,
       "idusuario", idusuario)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO pedidos(idnegocio, fecha, idusuario, valor, iva) VALUES(%s, %s, %s, %s, %s)",(int(idnegocio), fecha, int(idusuario), valor, iva))
        mysql.connection.commit()
        #se extrae el ultimo id del pedido insertado
        id =  cur.execute("select @@identity id from pedidos")
        print("se extrae el ultimo id del pedido insertado", id)
        cur.close()
        return jsonify({"datos":True, "id_pedido":id, "id_negocio":idnegocio, "feche":fecha, "id_usuario":idusuario, "Valor_total":valor, "iva":iva}),200
      

#registro detalles del pedido
class RegistroDetallesPedido(MethodView):
    def post(self):
        content = request.get_json()
        detallesPedido = content.get("pedidoDetalles")
        nombre = content.get("nombre")
        apellido = content.get("apellidos")
        negocio = content.get("negocio")
        iva = content.get("iva")
        total = content.get("total")
        print(negocio)
        documento = content.get("documento")
        for claveDetallaes in detallesPedido:

            if 'id' in claveDetallaes:
                idProducto = claveDetallaes['id']

            if 'precio' in claveDetallaes:
                valorProducto = claveDetallaes['precio']

            if 'cantidad' in claveDetallaes:
                cantidadProducto = claveDetallaes['cantidad']

            if 'iva' in claveDetallaes:
                ivaProducto = claveDetallaes['iva']

            if 'idPedido' in claveDetallaes:
                idPedido = claveDetallaes['idPedido']

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO detalles_pedidos(idproducto, valorunit, cantidad, iva, idpedido) VALUES(%s, %s, %s, %s, %s)",(idProducto, valorProducto, cantidadProducto, ivaProducto, idPedido))
            mysql.connection.commit()
        messager = 'INFORMACION DEL PEDIDO\nInformacion del usuario\nNombre : '+nombre+"\nApellido : "+apellido+"\nDocumento : "+documento+"\n"
        for add in detallesPedido:
            iva = str(add['iva'])
            precio = str(add['precio'])
            cantidad = str(add['cantidad'])
            text = str("Nombre del producto : "+add['nombre']+"\t Precio iva : "+iva+"\t Precio : "+precio+"\t cantidad : "+cantidad+"\n")
            messager += text
        iva = str(iva)
        total = str(total)
        messager += "IVA : "+iva+"\n"
        messager += "TOTAL : "+total+"\n"
        subject = 'Mensaje de click'
        messager = 'Subject : {}\n\n{}'.format(subject,messager)
        serve = smtplib.SMTP('smtp.gmail.com',587)
        serve.starttls()
        serve.login('clickproyecto791@gmail.com','click12345')
        serve.sendmail('clickproyecto791@gmail.com',negocio,messager)
        return jsonify({"datos":True, "id_producto":idProducto, "valor_producto":valorProducto, "cantidad_producto":cantidadProducto, "iva_producto":ivaProducto, "id_pedido":idPedido}),200


#pedir id del pedido
class pedirIdPedido(MethodView):
    def get(self):
        cur = mysql.connection.cursor()
        cur.execute("SELECT idpedido, idnegocio, fecha, idusuario, valor, iva FROM pedidos;")
        datosPedido = cur.fetchall()
        pedidoData = []
        datos = {}
        for idPedido in datosPedido:
            datos = {"id_pedido":idPedido[0]}
            pedidoData.append(datos)
            datos = {}
        return jsonify({"status":True, "datos_pedido": pedidoData })



#Actualizar usuario
class ActualizarUser(MethodView):
    def post(self):
        time.sleep(2)
        content = request.get_json()
        nombres = content.get("nombres")
        apellidos = content.get("apellidos")
        telefono = content.get("telefono")
        correo=content.get("correo")
        try:
            cur = mysql.connection.cursor()
            cur.execute(
            """
            UPDATE usuario
            SET nombres = %s, apellidos= %s, numtelefono= %s
            WHERE correo = %s;
            """,([nombres,apellidos,telefono,correo]))
            mysql.connection.commit()
            cur.close()            
            return jsonify({"datos": True, "nombre":nombres,"apellidos":apellidos,"numero":telefono}),200
        except:
            return jsonify({"datos":False}),403


#Eliminar usuario
class DeleteUser(MethodView):
    def post(self):
        content = request.get_json()
        correo=content.get("correo")
        try:
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM usuario WHERE correo = %s",([correo]))
            mysql.connection.commit()
            cur.close()
            return jsonify({"status": True}),200
        except:
            return jsonify({"status": False}),500

#Consultar negocios del usuario
class ConsultarNegocioUser(MethodView):
    def post(self):
        content=request.get_json()
        correo=content.get("correo")
        print(correo)
        try:
            cur=mysql.connection.cursor()
            cur.execute("""SELECT n.id,u.id FROM usuario u , negocio n
            where n.idusuario = u.id and u.correo = %s;""",([correo]))
            datos = cur.fetchall()
            print(datos[0])
            return jsonify({"status": True,"data":datos}),200
        except:
           return jsonify({"status": False}),500


class LoginUserControllers(MethodView):
    """
        Example Login
    """
    def post(self):
        time.sleep(2)
        #donde almacenan los datos de la base de datos
        datos = ""
        #simulacion de espera en el back con 1.5 segundos
        #config de json
        content = request.get_json()
        #traigo el objeto
        correo = content.get("email")
        password = content.get("password")
        cur=mysql.connection.cursor()
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
                
                return jsonify({"status": "Login exitoso", "id_usuario":datos[0], "correo":datos[1], "nombres":datos[2], "apellidos":datos[3], "tipo_documento":datos[4], "numero_documento":datos[5], "fecha_nacimiento":datos[6], "numero_telefono":datos[7], "token": encoded_jwt})
            else:
                return jsonify({"status": "Usuario y contraseña no validos"}), 400
        else:    
            return jsonify({"auth": False}), 400

class DatosEmpresa(MethodView):
    def get(self):
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, nombrenegocio, tipo, direccion, horarios, telefono1, telefono2, correo, idusuario, logo FROM negocio ;")
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
        print("ID DEL FRONT:", id)

        cur = mysql.connection.cursor()
        cur.execute("SELECT id, nombrenegocio, tipo, direccion, horarios, telefono1, telefono2, correo, idusuario, logo FROM negocio WHERE id = %s;",[(id)])
        datos = cur.fetchall()
        print("ESTOS SON LOS DATOS DEL NEGOCIO: ", datos)
        
        datosNegocio = []
        contentNegocio = {}
        for data in datos:
            contentNegocio = { 'id':data[0], 'nombre':data[1], 'tipo_negocio':data[2], 'direccion':data[3], 'horarios':data[4], 'telefono1':data[5], 'telefono2':data[6], 'correo':data[7], 'id_usuario': data[8], 'imgLogo':data[9] }
            datosNegocio.append(contentNegocio)
            return jsonify({'data':id, 'negocio_id':datosNegocio })


class ProductosEmpresa(MethodView):
    def post(self):
        content = request.get_json()
        id = content.get("id")
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, foto, nombre, precio, idnegocio, iva FROM producto WHERE idnegocio = %s;", [(id)])
        productos = cur.fetchall()
        cur.close()
        datos = []

        content = {}
        for valor in productos: 
            content = {'id':valor[0], 'foto':valor[1], 'nombre':valor[2], 'precio':valor[3], 'idnegocio':valor[4], 'iva':valor[5]}
            datos.append(content)
            content = {}
        #print("DATO0S DE PRODUCTOS DESDE LA BD: ", datos)
        
        return jsonify({"ok":True, "data": datos})


class EnviarProductos(MethodView):
    def post(self):
        content = request.get_json()
        data = content.get("data")
        cur=mysql.connection.cursor()
        print("DATOS DEL FRONTEND:",data)
        cur.execute('SELECT id, foto, nombre, precio, idnegocio, FROM producto WHERE idnegocio = 1 AND id = %s',([id]))
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
            content = {'id':result[0], 'nombre':result[1], 'ulrImg':result[2]}
            payload.append(content)
            content = {}
        return jsonify({"datos": payload}),200

#Clase que nos permite descriptar el token
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
            cur = mysql.connection.cursor()
            
            #ejecutar comandos de MySQL
            cur.execute("INSERT INTO  reservacion(cel,fecha,personas,idusuario) VALUES(%s,%s,%s,%s)",(cel,fecha,personas,idusuario))
            #actualiza la informacion que acaba de ingresar 
            mysql.connection.commit()
            #cerrar la conecion
            cur.close()
            return jsonify({"data":True}),200
        except:
            return "Lo sentimos el registro ya se ha hecho antes "


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

#MODULO NEGOCIOS

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
#MOSTRAR NEGOCIOS EN ZONA DE ADMINISTRACION
class MostrarNegocios(MethodView):
    def post(self):
        content = request.get_json()
        correo = content.get('correo')
        print(correo)
        cur = mysql.connection.cursor()
        cur.execute("""
        SELECT n.id, n.nombrenegocio,
        n.tipo, n.direccion,n.horarios,
        n.telefono1,n.telefono2,
        n.correo,n.idusuario,n.logo FROM negocio n ,usuario u
        where n.idusuario = u.id and u.correo = %s;
        """,([correo])
        )
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
        time.sleep(3)
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
        #Correo del usuario
        correo = content.get("correo")
        #Horario de la empresa 
        horario = content.get("horario")
        logo = content.get("logo")
        cur=mysql.connection.cursor()
        cur.execute('select id from usuario where correo = %s',([correo]))
        datos = cur.fetchall()
        id_usuario = 0
        for add in datos:
            print(add[0])
            id_usuario = add
        cur.execute("""
        insert into negocio(nombrenegocio,tipo,direccion,telefono1,telefono2,correo,idusuario,horarios,logo)
        values
        (%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """,(nombre,tipoE,direccionE,int(numeroE),int(numeroS),emailE,id_usuario,horario,logo))
        mysql.connection.commit()
        cur.close()
        return jsonify({"data": True}),200



class ActualizarNegocio(MethodView):
    def post(self):
        time.sleep(1)
        try:
            content = request.get_json()
            id_e = content.get("idn")
            nombre = content.get("nombre")
            tipo_empresa = content.get("tipo")
            direccion = content.get("direccion")
            telefono_principal = content.get("telefono1")
            telefono_secundario = content.get("telefono2")
            horarios = content.get("horarios")
            correo = content.get("correo")
            cur = mysql.connection.cursor()
            cur.execute("""
            UPDATE negocio SET nombrenegocio = %s, tipo = %s, direccion = %s, horarios = %s, telefono1 = %s, telefono2 = %s, correo = %s
            WHERE id = %s;""",(nombre, tipo_empresa, direccion, horarios, telefono_principal, telefono_secundario, correo, id_e))
            mysql.connection.commit()
            cur.close()
            return jsonify({"Se ha actualizado correctamente": True}),200
        except:
            return jsonify({"static":False}),403

class EliminarNegocio(MethodView):
    def delete(self):
        try:
            id_negocio = request.args.get('id')
            print("ELIMINAR ",id_negocio) 
            cur = mysql.connection.cursor()
            cur.execute('DELETE FROM negocio WHERE id = %s;',([int(id_negocio)]))
            mysql.connection.commit()
            cur.close()
            return jsonify({"data": True}),200
        except:
            return jsonify({"data":False}),500
        

#MODULO DE PRODUCTOS

class MostrarProductosNegocio(MethodView):
    def get(self):
        id_negocio = request.args.get('id')
        print(id_negocio)
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, foto, nombre, precio, iva FROM producto WHERE idnegocio = %s;",([id_negocio]))
        productos = cur.fetchall()
        cur.close()
        datos = []
        content = {}
        for valor in productos:
            content = {'id':valor[0], 'foto':valor[1], 'nombre':valor[2], 'precio':valor[3], 'iva':valor[4]}
            datos.append(content)
            content = {}
        return jsonify({"Obtener Productos": True, "data": datos}),200

class ProductoId(MethodView):
    def get(self):
        id_producto = request.args.get('id')
        #print(id_producto)
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, foto, nombre, precio,iva FROM producto WHERE id = %s;",([id_producto]))
        producto = cur.fetchall()
        cur.close()
        datos = []
        content = {}
        for valor in producto:
            content = {'id':valor[0], 'foto':valor[1], 'nombre':valor[2], 'precio':valor[3],'iva':valor[4]}
            datos.append(content)
            content = {}
        return jsonify({"Obtener producto": True, "data": datos}),200

#mofique esta parte
class CrearProducto(MethodView):
    def post(self):
        #try:
        content = request.get_json()
        foto = content.get("logo")
        nombre = content.get("nombre")
        precio = content.get("precio")
        id_negocio = content.get("idnegocio")
        iva = content.get('iva')
        print(id_negocio)
        print(nombre)
        print(iva)
        print(precio)
        cur = mysql.connection.cursor()
        cur.execute("""
        INSERT INTO producto (foto, nombre, precio, idnegocio,iva) VALUES (%s, %s, %s, %s, %s);
        """,(foto, nombre, float(precio), id_negocio, iva))
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
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE producto SET foto = %s, nombre = %s, precio = %s WHERE id = %s;
        """,(foto, nombre, precio,idproducto))
        mysql.connection.commit()
        cur.close()
        return jsonify({"Datos del producto actualizados exitosamente": True}), 200
        #except:


class EliminarProducto(MethodView):
    def post(self):
    #try:
        time.sleep(2)
        content = request.get_json()
        id_producto = content.get('id')
        print(id_producto)
        cur = mysql.connection.cursor()
        cur.execute("""
        DELETE FROM producto WHERE id = %s;
        """,([id_producto]))
        cur.execute("""
        DELETE FROM detalles_pedidos WHERE idproducto = %s;
        """,([id_producto]))
        
        mysql.connection.commit()
        cur.close()
        return jsonify({"Se ha eliminado el producto exitosamente": True}), 200
class EliminarTodoProducto(MethodView):
    def post(self):
        time.sleep(2)
        try:
            content = request.get_json()
            id_negocio = content.get('idNegocio') 
            print(id_negocio)
            cur =mysql.connection.cursor()
            cur.execute("""
            delete from producto where idnegocio =%s
            """,([id_negocio]))
            mysql.connection.commit()
            return jsonify({"status": True}), 200
        except:
            return jsonify({"status":False}),400
#Se debe pegar
class HistorialPedidos(MethodView):
    def post(self):
        time.sleep(1)
        content = request.get_json()
        correo = content.get('correo')
        cur = mysql.connection.cursor()
        cur.execute(
        """
        select p.valor,p.iva,p.fecha as FechaCompra,p.idpedido
        from pedidos  p ,negocio n
        where n.id = p.idnegocio
        and n.correo = %s
        order by p.fecha desc;
        """,([correo]))
        datas = cur.fetchall()
        print(datas)
        #cur.close()
        datos = []
        content = {}
        for valor in datas:
            content = {"valor":valor[0],"iva":valor[1],"fecha":valor[2],"noPedido":valor[3]
            }
            datos.append(content)

        return jsonify({'status':True,"data":datos}),200

class DetallesPedidos(MethodView):
    def post(self):
        time.sleep(1)
        content = request.get_json()
        idPedido = content.get('id')
        print("idPedido:",idPedido)
        cur = mysql.connection.cursor()
        cur.execute(
            """
            select u.numerodoc,u.tipodoc,
            u.nombres as NombreUser,
            u.apellidos,p.nombre,dp.cantidad,
            dp.valorunit,ps.valor,
            ps.iva from detalles_pedidos dp,
            pedidos ps,producto p,usuario u 
            where ps.idpedido = dp.idpedido and 
            p.id = dp.idproducto and u.id=ps.idusuario and ps.idpedido = %s;
            """,([idPedido])
        )
        data = cur.fetchall()
        cur.close()
        datos = []
        content = {}
        for valor in data:
            content = {"doc":valor[0],"tipoDoc":valor[1],
            "nombreUser":valor[2],"apellido":valor[3],
            "nombreProduct":valor[4],"cantidad":valor[5],"valorProduct": valor[6],"valor":valor[7],
            "iva":valor[8]
            }
            datos.append(content)
        print(datos)
        return jsonify({"data":datos})
