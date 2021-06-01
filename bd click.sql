CREATE SCHEMA bd_click; 
USE bd_click;

CREATE TABLE `usuario` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `correo` varchar(200) NOT NULL,
  `nombres` char(40) NOT NULL,
  `apellidos` char(40) NOT NULL,
  `tipodoc` char(2) NOT NULL,
  `numerodoc` char(10) NOT NULL,
  `fechanac` date NOT NULL,
  `numtelefono` CHAR(10) NOT NULL,
  `pass` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `correo` (`correo`)
);

INSERT INTO usuario(correo, nombres, apellidos, tipodoc, numerodoc, fechanac, numtelefono, pass) 
VALUES	('maicol@gmail.com', 'Maicol Fernando', 'Hernandez Peralta', 'CC', '1005367685', '2001-05-16', '30465625', 'djl3j2l4jdl3'),('maicolgomez420@gmail.com','maicol','hernandez gomez','CC','4566600','1999-06-28','312645577','jalñskañskdsk456');

SELECT * FROM usuario;


CREATE TABLE `negocio` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombrenegocio` char(50) NOT NULL,
  `tipo` char(40) NOT NULL,
  `direccion` varchar(200) NOT NULL,
  `horarios` varchar(100) NOT NULL,
  `telefono1` char(10) NOT NULL,
  `telefono2` char(10) NOT NULL,
  `correo` varchar(200) NOT NULL,
  `idusuario` int(11) NOT NULL,
  `logo` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `correo` (`correo`),
  KEY `idusuario` (`idusuario`),
  CONSTRAINT `negocio_ibfk_1` FOREIGN KEY (`idusuario`) REFERENCES `usuario` (`id`)
);


INSERT INTO `negocio` VALUES (1,'El buen sazon','comida','una casa','7am a 8pm','12314','243252','elbuensazon@gmail.com',1,'https://i.pinimg.com/originals/c2/bf/8f/c2bf8fe358f491df2bc6ebc34057172f.jpg'),(2,'Papitas enpolvadas','Camida Rapida','Calarca','7am a 11pm','32664466','888445','papitasenpolvadas@gmail.com',1,'https://img.freepik.com/vector-gratis/deliciosa-comida-rapida-estilo-pop-art_24908-61615.jpg');

SELECT * FROM negocio;


CREATE TABLE `producto` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `foto` text NOT NULL,
  `nombre` char(60) NOT NULL,
  `precio` double NOT NULL,
  `idnegocio` int(11) NOT NULL,
  `descripcion` char(200) NOT NULL,
  `iva` FLOAT NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idnegocio` (`idnegocio`),
  CONSTRAINT `producto_ibfk_1` FOREIGN KEY (`idnegocio`) REFERENCES `negocio` (`id`)
);



INSERT INTO producto(foto, nombre, precio, idnegocio, descripcion, iva) 
VALUES 	("https://s1.eestatic.com/2019/07/02/cocinillas/actualidad-gastronomica/actualidad_gastronomica_410720427_127098320_1280x1280.jpg"," Helado", 15000, 1,"Helado de bainilla",10),
		("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRU9D8uE6wcGL_YZrnv17Ef0Xl0Xn1syHLkWg&usqp=CAU", "Queso", 5000, 1, "El mejor queso, de la finca las golomdrinas",12),
        ("https://comercialgalera.com/wp-content/uploads/2015/06/0320-1.jpg", "Queso Crema", 8000, 1, "El mejor queso de la finca",13),
        ("https://jumbocolombiafood.vteximg.com.br/arquivos/ids/238190-1000-1000/7707192032385.jpg", "Leche de Coco", 5000, 1, "La mejor leche de coco",12),
		("https://admin.consumo.com.co/backend/admin/backend/web/archivosDelCliente/items/images/20200720084729-Lacteos-Refrigerados-Y-Congelados-Margarinas-y-Mantequillas-ESPARCIBLE-CAMPI-X-500-GR-PAISA-142202007200847293199.jpg", "Mantequilla Campi", 6000, 1, "La mejor mantequilla del campo",12),
        ("https://exitocol.vtexassets.com/arquivos/ids/5628097/Queso-Mozzarella-1231158_a.jpg", "Queso Mozzarella", 6000, 1, "El mejor queso mozzarella del campo",14),
        ("https://vixark.b-cdn.net/lp-i-i-g/yogur-griego-con-sabor-a-fresa-alpina-150g.jpg", "Yogur", 3000, 1, "Yogur griego de alpina",6),
        ("https://vixark.b-cdn.net/lp-i-i-g/yogur-griego-con-sabor-a-mora-alpina-160g-arándanos,-granola.jpg", "Yogur Griego", 2500, 1, "Yogur griego de alpina",12),
        
        ("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT3vKcjgVNV0DnWplH0bQzQswy-3bf-zhuphA&usqp=CAU", "Kumis", 2300, 1, "El mejor Kumis del campo",12),
        ("https://exitocol.vtexassets.com/arquivos/ids/4574282/QUESO-SANDUCHE-TAJADO-EXITO-MARCA-PROPIA-200-Gramo-424772_a.jpg", "Queso Sanduche ", 4600, 1, "El mejor queso sanduche",5),
        ("https://static.carrefour.es/hd_510x_/img_pim_food/193100_00_1.jpg", "Helado Chocolate", 12000, 1, "El mejor helado para disfrutar en familia",8),
        ("https://images.rappi.com.mx/products/977086784-1580932848675.png", "Mantequilla", 7000, 1, "La mejor matequilla para disfrutar en familia",3);


CREATE TABLE `pedidos` (
  `idpedido` int(11) NOT NULL AUTO_INCREMENT,
  `idnegocio` int(11) DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  `idusuario` int(11) DEFAULT NULL,
  `valor` FLOAT DEFAULT NULL,
  `iva` FLOAT NOT NULL,
  `estado` char(1) DEFAULT NULL,
  PRIMARY KEY (`idpedido`),
  KEY `idusuario` (`idusuario`),
  KEY `idnegocio` (`idnegocio`),
  CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`idusuario`) REFERENCES `usuario` (`id`),
  CONSTRAINT `pedidos_ibfk_2` FOREIGN KEY (`idnegocio`) REFERENCES `negocio` (`id`)
);



CREATE TABLE `detalles_pedidos` (
  `iddetallep` int(11) NOT NULL AUTO_INCREMENT,
  `idpedido` int(11) NOT NULL,
  `idproducto` int(11) NOT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `valorunit` float DEFAULT NULL,
  PRIMARY KEY (`iddetallep`),
  KEY `idpedido` (`idpedido`),
  KEY `idproducto` (`idproducto`),
  CONSTRAINT `detalles_pedidos_ibfk_1` FOREIGN KEY (`idpedido`) REFERENCES `pedidos` (`idpedido`),
  CONSTRAINT `detalles_pedidos_ibfk_2` FOREIGN KEY (`idproducto`) REFERENCES `producto` (`id`)
);


