"""<<<<<<< HEAD

app.add_url_rule(user["pedido_user"], view_func=user["pedido_user_controllers"])
app.add_url_rule(user["login_user"], view_func=user["login_user_controllers"])
app.add_url_rule(user["data_empresa"], view_func=user["data_empresa_controllers"])
app.add_url_rule(user["producto_empresa"], view_func=user["producto_empresa_controllers"])
app.add_url_rule(user["Register_user"], view_func=user["login_register_controllers"])
app.add_url_rule(user["Productos_clients"],view_func=user["productos"])
app.add_url_rule(user["Productos_clients_pedidos"],view_func=user["productosPedidos"])
app.add_url_rule(user["Reservar_user"],view_func=user["reservar_user_controllers"])
app.add_url_rule(user["Productos_id"],view_func=user["IdProduct"])
app.add_url_rule(user["PedidosUser"],view_func=user["pedidosUsers"])
app.add_url_rule(user["ActualizarProducto"],view_func=user["update"])
app.add_url_rule(user["delenteProduct"],view_func=user["Productdelete"])
app.add_url_rule(user["AgregarProduct"],view_func=user["insertProduct"])
======="""
from flask import Flask
from routes import *
from flask_cors import CORS
from routes import app
CORS(app, resources={r"/*": {"origins": "*"}})

app.add_url_rule(user["pedido_user"], view_func=user["pedido_user_controllers"])
app.add_url_rule(user["login_user"], view_func=user["login_user_controllers"])
app.add_url_rule(user["data_empresa"], view_func=user["data_empresa_controllers"])
app.add_url_rule(user["data_empresa_id"], view_func=user["data_empresa_id_controllers"])

app.add_url_rule(user["producto_empresa"], view_func=user["producto_empresa_controllers"])
app.add_url_rule(user["enviar_productos"],view_func=user["enviar_productos_controllers"])
app.add_url_rule(user["Register_user"], view_func=user["login_register_controllers"])
app.add_url_rule(user["Register_empresa"],view_func=user["registerEmpresa_controllers"])
app.add_url_rule(user["Productos_clients"],view_func=user["productos"])
app.add_url_rule(user["Productos_clients_pedidos"],view_func=user["productosPedidos"])
app.add_url_rule(user["Reservar_user"],view_func=user["reservar_user_controllers"])

app.add_url_rule(user["PedidosUser"],view_func=user["pedidosUsers"])
app.add_url_rule(user["ActualizarProducto"],view_func=user["update"])
app.add_url_rule(user["delenteProduct"],view_func=user["Productdelete"])
app.add_url_rule(user["AgregarProduct"],view_func=user["insertProduct"])

""">>>>>>> 9c56db8ebc849b2f157b7e93a4c432a735e4dd00
"""