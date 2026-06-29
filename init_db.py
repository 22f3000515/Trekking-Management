from app import app
from models import db,User
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    print("Database tables created successfully.")

    admin=User.query.filter_by(email='admin@trek.com').first()
    if not admin:
        admin=User(
            name='Admin',
            email='admin@trek.com',
            password=generate_password_hash('admin123'),
            role='admin',
            status='approved'
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully.")
        print("email:admin@trek.com")
        print("password:admin123")

    else:
        print("Admin user already exists.")
print("Database initialization completed.")   