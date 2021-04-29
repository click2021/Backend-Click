from flask import Flask
from routes import *
from flask_cors import CORS
from routes import app
CORS(app, resources={r"/*": {"origins": "*"}})
app.add_url_rule(routes["pedido"], view_func=routes["pedido_controllers"])
app.add_url_rule(user["login_user"], view_func=user["login_user_controllers"])
app.add_url_rule(user["Register_user"], view_func=user["login_register_controllers"])
app.add_url_rule(user["Productos_clients"],view_func=user["productos"])
app.add_url_rule(user["Productos_clients_pedidos"],view_func=user["productosPedidos"])
app.add_url_rule(user["Reservar_user"],view_func=user["reservar_user_controllers"])
app.add_url_rule(user["Productos_id"],view_func=user["IdProduct"])
app.add_url_rule(user["PedidosUser"],view_func=user["pedidosUsers"])
app.add_url_rule(user["ActualizarProducto"],view_func=user["update"])
app.add_url_rule(user["delenteProduct"],view_func=user["Productdelete"])
app.add_url_rule(user["AgregarProduct"],view_func=user["insertProduct"])