Web Base Template 1.0

Description

Web Base Template 1.0 is an application designed to serve as a solid starting point for developing robust web applications. Its modular and well-organized structure allows developers to focus on implementing specific features like e-commerce, blogs, or booking systems without worrying about tedious or repetitive initial setups.

This template includes:

    Secure authentication.
    User management system with roles.
    Scalable architecture.
    Database integration with PostgreSQL.
    Support for AJAX and responsive designs.

Technologies Used

    Python (Flask): Backend framework.
    PostgreSQL: Database.
    HTML5, CSS3, JavaScript: Front-end technologies.
    Bootstrap (local): Responsive styling.
    AJAX: Enhancing user experience with asynchronous interactions.
    Jinja2: Template engine.
    Werkzeug: Secure password management.
    Flask-Login, Flask-WTF, Flask-Mail: Extensions for authentication and forms.

Key Features

    Authentication System:
        User registration.
        Login.
        Password recovery with retry limits.

    User Management:
        CRUD for administrators.
        Roles and permissions.

    Note: The user addition and editing forms are not strictly validated as the registration form. This is to provide administrators with more flexibility, requiring caution to avoid creating temporary or unverified accounts, which could be a vulnerability for the application.

    Admin Dashboard:
        Pagination and search.

    Modular Architecture:
        Clear division of routes and blueprints.

    Professional Database:
        Scalable and secure design with PostgreSQL.

Installation and Setup
Prerequisites

    Python 3.9 or higher.
    PostgreSQL.
    Configured virtual environment.

Installation Steps

    Clone the repository:

git clone <REPOSITORY_URL>
cd web-base-template-1.0

Set up the virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Set up environment variables:
Create a .env file in the root directory with the following variables:

FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=<your_secret_key>
SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://<username>:<password>@<host>/<db_name>
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=<email>
MAIL_PASSWORD=<password>

Initialize the database:

flask db upgrade

Run the application:

    python run.py

The application will be available at http://127.0.0.1:5000.
General Project Structure

web-base-template-1.0/
├── app
│   ├── __init__.py
│   ├── models.py
│   ├── routes
│   ├── static
│   └── templates
├── config.py
├── migrations
│   ├── alembic.ini
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions
├── README.md
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

Contribution

Contributions are welcome via pull requests. Please ensure your code follows best practices and passes all tests before submitting.
License

This project is licensed under the MIT License.

Note: Although this project works 100%, it is recommended to review and test the code before using it in production. Its primary purpose is to professionally facilitate the work of beginner developers starting with Flask.
Donations

If you’d like to support this project, consider making a cryptocurrency donation.

    USDT (TRC20): [TJHmU2QVHs8QTXBnfpk97LH7Mpb2CyZ8cA]

Thank you for your support! 🙌