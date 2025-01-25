# Plantilla Web Base 1.0

## Descripción

**Plantilla Web Base 1.0** es una aplicación diseñada para servir como punto de partida sólido para el desarrollo de aplicaciones web robustas. Su estructura modular y bien organizada permite a los desarrolladores concentrarse en la implementación de funcionalidades específicas, como e-commerce, blogs o sistemas de reservas, sin preocuparse por configuraciones iniciales tediosas o repetitivas.

Esta plantilla incluye:

- Autenticación segura.
- Sistema de gestión de usuarios con roles.
- Arquitectura escalable.
- Integración de base de datos con PostgreSQL.
- Soporte para AJAX y diseños responsivos.

## Tecnologías Utilizadas

- **Python** (Flask): Framework backend.
- **PostgreSQL**: Base de datos.
- **HTML5**, **CSS3**, **JavaScript**: Tecnologías front-end.
- **Bootstrap** (local): Estilos responsivos.
- **AJAX**: Mejora de la experiencia de usuario con interacciones asíncronas.
- **Jinja2**: Motor de plantillas.
- **Werkzeug**: Gestión de contraseñas seguras.
- **Flask-Login**, **Flask-WTF**, **Flask-Mail**: Extensiones para autenticación y formularios.

## Características Principales

1. **Sistema de Autenticación**:

   - Registro de usuarios.
   - Inicio de sesión.
   - Recuperación de contraseñas con límites de reenvío.

2. **Gestión de Usuarios**:

   - CRUD para administradores.
   - Roles y permisos.

   nota: Los formularios de adición y edición de usuarios no estan validados obligatoriamente
         como es el caso del formulario de registro. esto es para que el administrador tenga más
         flexibilidad de manera general, lo cual requiere mas atención y cuidado de no crear cuentas
         temporales, o no verificadas que puedan ser una vulnerabilidad para la aplicación.

3. **Panel de Administración**:

   - Paginación y buscador.

4. **Arquitectura Modular**:

   - División clara de rutas y blueprints.

5. **Base de Datos Profesional**:

   - Diseño escalable y seguro con PostgreSQL.

## Instalación y Configuración

### Requisitos Previos

- Python 3.9 o superior.
- PostgreSQL.
- Entorno virtual configurado.

### Pasos de Instalación

1. **Clonar el repositorio**:

   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd plantilla-web-base-1.0
   ```

2. **Configurar el entorno virtual**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**:
   Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

   ```env
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=<clave_secreta>
   SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://<usuario>:<contraseña>@<host>/<nombre_db>
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=<correo>
   MAIL_PASSWORD=<contraseña>
   ```

5. **Inicializar la base de datos**:

   ```bash
   flask db upgrade
   ```

6. **Ejecutar la aplicación**:

   ```
   bash
   python3 run.py
   ```

   ```
   cmd
   python run.py
   ```

La aplicación estará disponible en [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Estructura del General del Proyecto

```
plantilla-web-base-1.0/
├── app
│   ├── __init__.py
│   ├── models.py
│   ├── routes
│   ├── static
│   └── templates
├── config.py
├── migrations
│   ├── alembic.ini
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions
├── readme.md
├── requirements.txt
├── run.py
└── utils
    ├── admin_default_generator.py
    ├── change_password_postgres.py
    ├── __init__.py
    ├── logging_config.py
    ├── postgres_query.py
    ├── pruebas.py
    └── random_password_generator.py
```

## Contribución

Se aceptan contribuciones mediante pull requests. Por favor, asegúrate de que tu código siga las mejores prácticas y pase las pruebas antes de enviarlo.

## Licencia

Este proyecto está licenciado bajo la [MIT License](LICENSE).

**Nota**: Aunque este proyecto funciona al 100%, se recomienda revisar y probar el código antes de usarlo en producción. Su propósito principal es facilitar el trabajo de desarrolladores principiantes de forma profesional que comienzan a usar Flask.


## Donaciones

Si deseas apoyar este proyecto, considera realizar una donación en criptomonedas.

- **USDT (TRC20)**: *[TJHmU2QVHs8QTXBnfpk97LH7Mpb2CyZ8cA]*

¡Gracias por tu apoyo! 🙌


