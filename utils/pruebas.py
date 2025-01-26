from flask_bcrypt import Bcrypt

#import sys
#import os

# Add the path to the project's root directory
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

bcrypt = Bcrypt()

# Example hash
hashed_password = bcrypt.generate_password_hash("admin123").decode('utf-8')
print(f"Generated hash: {hashed_password}")

# Verification
is_valid = bcrypt.check_password_hash(hashed_password, "admin123")
print(f"Is the password valid? {is_valid}")

