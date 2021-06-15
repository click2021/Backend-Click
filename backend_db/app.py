from flask import Flask, views
from routes import *
from flask_cors import CORS
from routes import app
CORS(app, resources={r"/*": {"origins": "*"}})

#Consultar negocio del usuario
app.add_url_rule(user["consultar_negocio_user"],view_func=user["consultar_negocio_user_controllers"])
#Actualizar usuario
app.add_url_rule(user["actualizar_user"],view_func=user["actualizar_user_controllers"])
#eliminar usuario
app.add_url_rule(user["delete_user"],view_func=user["delete_user_controllers"])
app.add_url_rule(user["pedido_user"], view_func=user["pedido_user_controllers"])
app.add_url_rule(user["login_user"], view_func=user["login_user_controllers"])
app.add_url_rule(user["data_empresa"], view_func=user["data_empresa_controllers"])
app.add_url_rule(user["data_empresa_id"], view_func=user["data_empresa_id_controllers"])

app.add_url_rule(user["producto_empresa"], view_func=user["producto_empresa_controllers"])
app.add_url_rule(user["enviar_productos"],view_func=user["enviar_productos_controllers"])
app.add_url_rule(user["registro_user"], view_func=user["user_registro_controllers"])
app.add_url_rule(user["Productos_clients"],view_func=user["productos"])

app.add_url_rule(user["Productos_clients_pedidos"],view_func=user["productosPedidos"])
app.add_url_rule(user["Reservar_user"],view_func=user["reservar_user_controllers"])
app.add_url_rule(user["PedidosUser"],view_func=user["pedidosUsers"])
app.add_url_rule(user["ActualizarProducto"],view_func=user["update"])
app.add_url_rule(user["delenteProduct"],view_func=user["Productdelete"])
app.add_url_rule(user["AgregarProduct"],view_func=user["insertProduct"])

#modulo negocio
app.add_url_rule(user["mostrar_todos_negocios"],view_func=user["negocios"])
app.add_url_rule(user["mostrar_negocio"],view_func=user["negocio"])
app.add_url_rule(user["mostrar_negocios"],view_func=user["mostrarNegocios"])
app.add_url_rule(user["mostrar_negocio_id"],view_func=user["mostrarNegocioId"])
app.add_url_rule(user["register_empresa"],view_func=user["registerEmpresa_controllers"])
app.add_url_rule(user["actualizar_negocio"],view_func=user["actualizarNegocio"])
app.add_url_rule(user["eliminar_negocio"],view_func=user["eliminarNegocio"])

#modulo producto
app.add_url_rule(user["mostrar_productos"],view_func=user["mostrarProductos"])
app.add_url_rule(user["producto_id"],view_func=user["productoId"])
app.add_url_rule(user["crear_producto"],view_func=user["crearProducto"])
app.add_url_rule(user["actualizar_producto"],view_func=user["actualizarProducto"])
app.add_url_rule(user["eliminar_producto"],view_func=user["eliminarProducto"])
app.add_url_rule(user["eliminar_todo_p"],view_func=user["eliminarTodosP"])