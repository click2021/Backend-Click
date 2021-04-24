from controllers import LoginUserControllers,RegisterUserControllers,Productos,app,PedidosUserControllers,ReservarUserControllers
from controllers import updateProduct,delete,ProductosId,PedidosUser,agregar

user = {
    "login_user": "/api/v01/user/login", "login_user_controllers": LoginUserControllers.as_view("login_api"),
    "Register_user": "/api/v01/user/register", "login_register_controllers": RegisterUserControllers.as_view("register_api"),
    "Productos_clients":"/api/v01/user/product","productos":Productos.as_view("productos_api"),
    "Productos_clients_pedidos":"/api/v01/user/getInfo","productosPedidos":PedidosUserControllers.as_view("pedidos"),
    "Reservar_user":"/api/v01/user/reservar","reservar_user_controllers":ReservarUserControllers.as_view("reservar_api"),
    "Productos_id":"/api/v01/user/get","IdProduct":ProductosId.as_view("producto_Id"),
    "PedidosUser":"/api/v01/user/pedido","pedidosUsers":PedidosUser.as_view("api_pedidos"),
    "ActualizarProducto":"/api/v02/user/updateProduct","update":updateProduct.as_view('update_product'),
    "delenteProduct":"/api/v02/user/deleteProduct","Productdelete":delete.as_view("delenteProduct_api"),
    "AgregarProduct":"/api/v02/user/agregar","insertProduct":agregar.as_view("agregar_api"),
}

