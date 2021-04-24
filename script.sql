create table usuarios(
nombre char(80),
apellido char(90),
email varchar(200) primary key not null,
administrador char(1),
clave text not null
) engine='InnoDB'default charset = latin1;

CREATE TABLE productos(
id int primary key not null auto_increment,
titulo varchar(200),
urlImg text,
precio float
);
CREATE TABLE pedidos(
id int auto_increment primary key,
direccion varchar(300),
numeroSecudario char(16),	
cantidad int,
producto int,
correo varchar(200) not null,
fecha date
)engine='InnoDB'default charset = latin1;

ALTER TABLE pedidos
ADD FOREIGN KEY (correo) REFERENCES usuarios(email);

ALTER TABLE pedidos
ADD FOREIGN KEY (producto) REFERENCES productos(id);



insert into productos (titulo,urlImg)
values("Sancocho","https://images-gmi-pmc.edge-generalmills.com/a32379ab-65fb-4242-9e07-28fbb087524e.jpg"),
("Ajiaco","https://antojandoando.com/wp-content/uploads/2015/01/ajiaco-close.jpg")
; 
insert into productos (titulo,urlImg,precio)
values
("Arroz Paisa","https://i.pinimg.com/736x/6b/09/e5/6b09e5fedf17b78b2504575dfc097cf0.jpg",7000),
("Crepes","https://okdiario.com/img/recetas/2016/05/01/crepes-01.jpg",10000),
("Ratatouille","https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTs9WL7TmQ0i6TNgZD5wwGomxsfDHtq1VZG9w&usqp=CAU",7000),
("Confit de pato","https://s1.eestatic.com/2018/12/12/cocinillas/cocinillas_360228696_116637031_1024x576.jpg",8000),
("Bandeja Paisa","https://cdn.colombia.com/gastronomia/2011/08/02/bandeja-paisa-1616.gif",9000),
("Empanadas","https://i.pinimg.com/originals/e2/62/79/e26279025e32b49018934d08bf653e14.jpg",100000),
("Cassoulet","https://www.seriouseats.com/recipes/images/2014/10/20140930-cassoulet-recipe-food-lab-new-6.jpg",80000),
("Aligot","http://truffle-assets.imgix.net/661e969f-l.jpg?w=600&fl=progressive&auto=format,compress&cs=tinysrgb&dpr=1",7000),
("Gratin dauphinois","https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSly0rOgJrAhUnqBl9QuAEFzxvln9AjvPU7ow&usqp=CAU",5000),
("Quiche","https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRoijBYq1QPfmtyZtQ97rcDtpiixOv7lzvVmg&usqp=CAU",9000)
; 
create table reservacion(
id int(10) primary key auto_increment not null,
cel char(15),
fecha date,
personas int(50),
idusuario varchar(200) not null,
FOREIGN KEY (idusuario) REFERENCES usuarios (email)
) engine='InnoDB'default charset = latin1 ;