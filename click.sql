-- MariaDB dump 10.19  Distrib 10.4.18-MariaDB, for Win64 (AMD64)
--
-- Host: 127.0.0.1    Database: bd_click
-- ------------------------------------------------------
-- Server version	10.4.18-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `detalles_pedidos`
--

DROP TABLE IF EXISTS `detalles_pedidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalles_pedidos`
--

LOCK TABLES `detalles_pedidos` WRITE;
/*!40000 ALTER TABLE `detalles_pedidos` DISABLE KEYS */;
/*!40000 ALTER TABLE `detalles_pedidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `negocio`
--

DROP TABLE IF EXISTS `negocio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `negocio`
--

LOCK TABLES `negocio` WRITE;
/*!40000 ALTER TABLE `negocio` DISABLE KEYS */;
INSERT INTO `negocio` VALUES (1,'El buen sazon','comida','una casa','7am a 8pm','12314','243252','elbuensazon@gmail.com',1,'https://i.pinimg.com/originals/c2/bf/8f/c2bf8fe358f491df2bc6ebc34057172f.jpg'),(2,'Papitas enpolvadas','Camida Rapida','Calarca','7am a 11pm','32664466','888445','papitasenpolvadas@gmail.com',1,'https://img.freepik.com/vector-gratis/deliciosa-comida-rapida-estilo-pop-art_24908-61615.jpg');
/*!40000 ALTER TABLE `negocio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedidos`
--

DROP TABLE IF EXISTS `pedidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pedidos` (
  `idpedido` int(11) NOT NULL AUTO_INCREMENT,
  `idnegocio` int(11) DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  `idusuario` int(11) DEFAULT NULL,
  `valor` float DEFAULT NULL,
  `estado` char(1) DEFAULT NULL,
  PRIMARY KEY (`idpedido`),
  KEY `idusuario` (`idusuario`),
  KEY `idnegocio` (`idnegocio`),
  CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`idusuario`) REFERENCES `usuario` (`id`),
  CONSTRAINT `pedidos_ibfk_2` FOREIGN KEY (`idnegocio`) REFERENCES `negocio` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos`
--

LOCK TABLES `pedidos` WRITE;
/*!40000 ALTER TABLE `pedidos` DISABLE KEYS */;
/*!40000 ALTER TABLE `pedidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto`
--

DROP TABLE IF EXISTS `producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `producto` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `foto` text NOT NULL,
  `nombre` char(60) NOT NULL,
  `precio` double NOT NULL,
  `idnegocio` int(11) NOT NULL,
  `descripcion` char(200) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idnegocio` (`idnegocio`),
  CONSTRAINT `producto_ibfk_1` FOREIGN KEY (`idnegocio`) REFERENCES `negocio` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto`
--

LOCK TABLES `producto` WRITE;
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
INSERT INTO `producto` VALUES (1,'https://s1.eestatic.com/2019/07/02/cocinillas/actualidad-gastronomica/actualidad_gastronomica_410720427_127098320_1280x1280.jpg',' Helado',15000,1,'Helado de bainilla'),(2,'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRU9D8uE6wcGL_YZrnv17Ef0Xl0Xn1syHLkWg&usqp=CAU','Queso',5000,1,'El mejor queso, de la finca las golomdrinas'),(3,'https://comercialgalera.com/wp-content/uploads/2015/06/0320-1.jpg','Queso Crema',8000,1,'El mejor queso de la finca'),(4,'https://jumbocolombiafood.vteximg.com.br/arquivos/ids/238190-1000-1000/7707192032385.jpg','Leche de Coco',5000,1,'La mejor leche de coco'),(5,'https://admin.consumo.com.co/backend/admin/backend/web/archivosDelCliente/items/images/20200720084729-Lacteos-Refrigerados-Y-Congelados-Margarinas-y-Mantequillas-ESPARCIBLE-CAMPI-X-500-GR-PAISA-142202007200847293199.jpg','Mantequilla Campi',6000,1,'La mejor mantequilla del campo'),(6,'https://exitocol.vtexassets.com/arquivos/ids/5628097/Queso-Mozzarella-1231158_a.jpg','Queso Mozzarella',6000,1,'El mejor queso mozzarella del campo'),(7,'https://vixark.b-cdn.net/lp-i-i-g/yogur-griego-con-sabor-a-fresa-alpina-150g.jpg','Yogur Griego',3000,1,'Yogur griego de alpina'),(8,'https://vixark.b-cdn.net/lp-i-i-g/yogur-griego-con-sabor-a-mora-alpina-160g-arándanos,-granola.jpg','Yogur Griego',2500,1,'Yogur griego de alpina'),(9,'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT3vKcjgVNV0DnWplH0bQzQswy-3bf-zhuphA&usqp=CAU','Kumis',2300,1,'El mejor Kumis del campo'),(10,'https://exitocol.vtexassets.com/arquivos/ids/4574282/QUESO-SANDUCHE-TAJADO-EXITO-MARCA-PROPIA-200-Gramo-424772_a.jpg','Queso Sanduche',4600,1,'El mejor queso sanduche'),(11,'https://static.carrefour.es/hd_510x_/img_pim_food/193100_00_1.jpg','Helado Chocolate',12000,1,'El mejor helado para disfrutar en familia'),(12,'https://images.rappi.com.mx/products/977086784-1580932848675.png','Mantequilla',7000,1,'La mejor matequilla para disfrutar en familia'),(13,'https://www.fincasturisticasdelquindio.com/wp-content/uploads/2016/10/Comida-rapida-armenia-755x566.jpg','Combo hamburgues',15000,2,'El mejor sabor de las hamburguesas'),(14,'https://cdn.kiwilimon.com/recetaimagen/13003/th5-640x426-5707.jpg','Pizaa ruleta',25000,2,'El mejor sabor de las de las pizzas de papitas enpolvadas');
/*!40000 ALTER TABLE `producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usuario` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `correo` varchar(200) NOT NULL,
  `nombres` char(40) NOT NULL,
  `apellidos` char(40) NOT NULL,
  `tipodoc` char(2) NOT NULL,
  `numerodoc` char(10) NOT NULL,
  `fechanac` date NOT NULL,
  `pass` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `correo` (`correo`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'maicolhernandez420@gmail.com','Maicol Fernando','Hernandez Peralta','CC','1005367685','2001-05-16','djl3j2l4jdl3'),(2,'maicolgomez420@gmail.com','maicol','hernandez gomez','CC','4566600','1999-06-28','jalñskañskdsk456');
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-05-18  9:07:48