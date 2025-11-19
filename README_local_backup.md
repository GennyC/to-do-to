# Do To Do - Sistema de Gestión de Tareas
Este es un sistema moderno de gestión de tareas personales desarrollado en Python, Flask, MySQL y JavaScript.
Permite a los usuarios organizar sus tareas de manera eficiente con una interfaz intuitiva y responsive.
## Funcionalidades
Gestión de Tareas
Crear nuevas tareas con título, descripción y fecha de vencimiento

Actualizar estado de tareas (To Do, In Progress, Done)

Eliminar tareas propias

Búsqueda en tiempo real de tareas

Organización Visual
Vista principal dividida en: Esta Semana, Este Mes, Todas las Tareas

Vistas filtradas por estado: To Do, In Progress, Done (organizadas por mes)

Diseño responsive con tarjetas visuales

Gestión de Usuario
Registro y autenticación segura

Actualización de perfil (nombre y contraseña)

Aislamiento de datos: cada usuario solo ve sus propias tareas

## Instalación
1. Clona este repositorio:
git clone https://github.com/GennyC/to-do-to.git
cd to-do-to
2. Crea un entorno virtual e instala dependencias:
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
3. Crea la base de datos en MySQL:
CREATE DATABASE to_do_app;
4. Importa la estructura inicial:
-- Tabla de usuarios
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de tareas
CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status ENUM('To Do', 'In Progress', 'Done') DEFAULT 'To Do',
    due_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INT NOT NULL
);

5. Configura la conexión a la base de datos en config.py:
MYSQL_HOST = "localhost"
MYSQL_USER = "tu_usuario"
MYSQL_PASSWORD = "tu_contraseña"
MYSQL_DB = "to_do_app"
6. Ejecuta la aplicación:
python app.py
7. Accede desde el navegador:
http://localhost:5001

## Despliegue en Producción
Servicios utilizados:
Heroku (Hosting): Despliegue de la aplicación Python/Flask

JawsDB MySQL (Base de datos en la nube): Addon de Heroku para la gestión de la base de datos

Gunicorn: Servidor WSGI para producción

## Estructura del Proyecto
to-do-to/
│── app.py              # Aplicación principal Flask
│── config.py           # Configuración de base de datos
│── models.py           # Modelos y consultas a la BD
│── requirements.txt    # Dependencias de Python
│── Procfile           # Configuración para Heroku
│── Dockerfile         # Configuración para Docker
│── docker-compose.yml # Orquestación de contenedores
│── static/
│   ├── styles.css     # Estilos CSS
│   └── app.js         # JavaScript del frontend
│── templates/
│   ├── base.html      # Layout principal
│   ├── home.html      # Página principal
│   ├── login.html     # Inicio de sesión
│   ├── register.html  # Registro de usuario
│   ├── account.html   # Gestión de cuenta
│   └── tasks_by_month.html # Vista de tareas por mes

##Tecnologías Utilizadas
Backend: Python, Flask, MySQL

Frontend: HTML5, CSS3, JavaScript, Jinja2

Base de datos: MySQL con mysql-connector-python

Autenticación: Flask sessions con hash de contraseñas

Despliegue: Heroku, JawsDB, Docker

Producción: Gunicorn WSGI server

