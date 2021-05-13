CREATE SCHEMA bd_click; 
USE bd_click;

CREATE TABLE usuario (
id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
correo VARCHAR(200) UNIQUE NOT NULL, 
nombres CHAR(40) NOT NULL,
apellidos CHAR(40) NOT NULL,
tipodoc CHAR(2) NOT NULL,
numerodoc CHAR(10)NOT NULL,
fechanac DATE NOT NULL,
pass TEXT NOT NULL
);

INSERT INTO usuario(correo, nombres, apellidos, tipodoc, numerodoc, fechanac, pass) 
VALUES 	("maicolhernandez420@gmail.com", "Maicol Fernando", "Hernandez Peralta", "CC", "1005367685", "2001-05-16", "djl3j2l4jdl3"),
		("maicolgomez420@gmail.com", "maicol", "hernandez gomez", "CC", "4566600", "1999-06-28", "jalñskañskdsk456" );


CREATE TABLE negocio (
id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
nombrenegocio CHAR(50) NOT NULL,
tipo CHAR(40) NOT NULL,
direccion VARCHAR(200) NOT NULL,
horarios VARCHAR(100) NOT NULL,
telefono1 CHAR(10) NOT NULL ,
telefono2 CHAR(10) NOT NULL,
correo VARCHAR(200) UNIQUE NOT NULL,
idusuario INT NOT NULL,
logo TEXT NOT NULL,
FOREIGN KEY (idusuario) REFERENCES usuario(id)
);


INSERT INTO negocio(nombrenegocio, tipo, direccion, horarios, telefono1, telefono2, correo, idusuario, logo) 
VALUES 	("El buen sazon", "comida", "una casa", "7am a 8pm", "12314", "243252", "elbuensazon@gmail.com", 1, "https://i.pinimg.com/originals/c2/bf/8f/c2bf8fe358f491df2bc6ebc34057172f.jpg"),
		("Papitas enpolvadas", "Camida Rapida", "Calarca", "7am a 11pm", "32664466", "888445", "papitasenpolvadas@gmail.com", 1, "https://img.freepik.com/vector-gratis/deliciosa-comida-rapida-estilo-pop-art_24908-61615.jpg");

SELECT id, nombrenegocio, tipo, direccion, horarios, telefono1, telefono2, correo, idusuario, logo FROM negocio
WHERE id=1;


SELECT * FROM negocio;

CREATE TABLE producto (
id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
foto TEXT NOT NULL,
nombre CHAR(60) NOT NULL,
precio DOUBLE NOT NULL,
idnegocio INT NOT NULL,
descripcion CHAR(200) NOT NULL,
FOREIGN KEY (idnegocio) REFERENCES negocio(id)
);


INSERT INTO producto(foto, nombre, precio, idnegocio, descripcion) 
VALUES 	("https://s1.eestatic.com/2019/07/02/cocinillas/actualidad-gastronomica/actualidad_gastronomica_410720427_127098320_1280x1280.jpg"," Helado", 15000, 1,"Helado de bainilla"),
		("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRU9D8uE6wcGL_YZrnv17Ef0Xl0Xn1syHLkWg&usqp=CAU", "Queso", 5000, 1, "El mejor queso, de la finca las golomdrinas"),
        ("https://comercialgalera.com/wp-content/uploads/2015/06/0320-1.jpg", "Queso Crema", 8000, 1, "El mejor queso de la finca"),
        ("https://jumbocolombiafood.vteximg.com.br/arquivos/ids/238190-1000-1000/7707192032385.jpg", "Leche de Coco", 5000, 1, "La mejor leche de coco"),
		("https://admin.consumo.com.co/backend/admin/backend/web/archivosDelCliente/items/images/20200720084729-Lacteos-Refrigerados-Y-Congelados-Margarinas-y-Mantequillas-ESPARCIBLE-CAMPI-X-500-GR-PAISA-142202007200847293199.jpg", "Mantequilla Campi", 6000, 1, "La mejor mantequilla del campo"),
        ("https://exitocol.vtexassets.com/arquivos/ids/5628097/Queso-Mozzarella-1231158_a.jpg", "Queso Mozzarella", 6000, 1, "El mejor queso mozzarella del campo"),
        ("https://vixark.b-cdn.net/lp-i-i-g/yogur-griego-con-sabor-a-fresa-alpina-150g.jpg", "Yogur Griego", 3000, 1, "Yogur griego de alpina"),
        ("https://vixark.b-cdn.net/lp-i-i-g/yogur-griego-con-sabor-a-mora-alpina-160g-arándanos,-granola.jpg", "Yogur Griego", 2500, 1, "Yogur griego de alpina"),
        
        ("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT3vKcjgVNV0DnWplH0bQzQswy-3bf-zhuphA&usqp=CAU", "Kumis", 2300, 1, "El mejor Kumis del campo"),
        ("https://exitocol.vtexassets.com/arquivos/ids/4574282/QUESO-SANDUCHE-TAJADO-EXITO-MARCA-PROPIA-200-Gramo-424772_a.jpg", "Queso Sanduche ", 4600, 1, "El mejor queso sanduche"),
        ("https://static.carrefour.es/hd_510x_/img_pim_food/193100_00_1.jpg", "Helado Chocolate", 12000, 1, "El mejor helado para disfrutar en familia"),
        ("https://images.rappi.com.mx/products/977086784-1580932848675.png", "Mantequilla", 7000, 1, "La mejor matequilla para disfrutar en familia");
          
INSERT INTO producto(foto, nombre, precio, idnegocio, descripcion) 
VALUES 	("https://www.fincasturisticasdelquindio.com/wp-content/uploads/2016/10/Comida-rapida-armenia-755x566.jpg", "Combo hamburgues", 15000, 2, "El mejor sabor de las hamburguesas"),
		("https://cdn.kiwilimon.com/recetaimagen/13003/th5-640x426-5707.jpg", "Pizaa ruleta", 25000, 2, "El mejor sabor de las de las pizzas de papitas enpolvadas");
        
        
SELECT * FROM producto;

SELECT id, foto, nombre, precio, idnegocio, descripcion FROM producto
WHERE idnegocio = 1 AND id = 2;

/*
CREATE TABLE comprador (
id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
nombres CHAR(40) NOT NULL,
apellidos CHAR(40) NOT NULL,
telefono CHAR(11) NOT NULL,
correo VARCHAR(200) NOT NULL UNIQUE,
direccion VARCHAR(200) NOT NULL,
idnegocio INT NOT NULL
FOREIGN KEY (idnegocio) REFERENCES negocio(id)
);
*/



SELECT * FROM negocio;

/*
INSERT INTO comprador(nombres, apellidos, telefono, correo, direccion, idnegocio)
VALUES	("MAICOL FERNANDO", "HERNANDEZ PERALTA", "16664455", "maicolhernandez420@gmail.com", "una casa", 1),
		("maicol", "hernandez gomez", "4566600", "maicolgomez420@gmail.com", "una casa", 1),
        ("Juan Sebastian", "Pulgarin Quintero", "463000", "juanpulgarin23@gmail.com", "Armenia", 2),
       ("Camilo", "Aguja Chico", "camiloaguja44@gmail.com", "
       5551221", "Armenia", 2); */

SELECT id, nombrenegocio, tipo, direccion, horarios, telefono1, telefono2, correo, idusuario, logo FROM negocio
WHERE id = 1;        
         
/*
CREATE TABLE pedidos (
id INT AUTO_INCREMENT NOT NULL 
);
*/

/*
CREATE TABLE detalles_pedidos(
id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
idproducto INT NOT NULL,
idpedido INT NOT NULL,
FOREIGN KEY (idpedido) REFERENCES pedidos(id),
FOREIGN KEY (idproducto) REFERENCES producto(id)
);*/
/*
CREATE TABLE detallesnegocio(
id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
idnegocio INT NOT NULL,
idpedido INT NOT NULL,
FOREIGN KEY (idnegocio) REFERENCES negocio(id),
FOREIGN KEY (idpedido) REFERENCES pedidos(id)
);*/

SELECT * FROM producto;
/*
INSERT INTO detalles_pedidos(idpedido, idproducto) 
VALUES	(3, 13),
		(3, 13),
		(3, 14),
        (1, 4),
        (1, 2),
producto        (4, 13),
        (4, 14);
      
*/

SELECT * FROM producto;

SELECT * FROM negocio;

/*
SELECT n.idempresario, n.id, n.nombrenegocio, pro.nombre as nombre_producto, pro.idnegocio as id_producto 
FROM negocio n, producto pro, pedidos p
WHERE n.id=pro.idnegocio and n.id=p.idnegocio;
*/

