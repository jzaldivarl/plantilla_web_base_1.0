# admin_default_generator.py #

#import sys
#import os

# Add the project root directory to the path
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db, bcrypt
from app.models import User

# Create the Flask app
app = create_app()

# Define the user fields to create in the DB
user = 'admin'
number = 2
generic_user = f'{user}{number}'
generic_email = f'{user}{number}@example.com'
generic_password = 'admin123'
generic_is_admin = True
generic_is_verified = True

with app.app_context():

    try:
        # Search for the user
        user = User.query.filter_by(username=generic_user).first()

        if user:
            # If exists, delete it
            db.session.delete(user)
            db.session.commit()
            print(f"User {generic_user} deleted.")

        # Create a new user
        new_user = User(
            username=generic_user,
            email=generic_email,
            password_hash=bcrypt.generate_password_hash(generic_password).decode('utf-8'),
            is_admin=generic_is_admin,
            is_verified=generic_is_verified
        )

        db.session.add(new_user)
        db.session.commit()
        print(f"User {generic_user} created successfully.")

    except Exception as e:
        print(f'The following error occurred:\n\n {str(e)} \n\n Please try to resolve it and try again')

