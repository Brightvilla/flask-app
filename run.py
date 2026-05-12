from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from app.models.user import User
from app.models.products import Product

app = create_app()

def init_db():
    db.create_all()

    if User.query.first() is None:
        admin = User(username="admin", email="admin@test.com", role="admin")
        admin.set_password("password")

        user = User(username="user", email="user@test.com", role="user")
        user.set_password("password")

        db.session.add_all([admin, user])

        db.session.add_all([
            Product(name="Laptop", price=50000, stock=10),
            Product(name="Phone", price=20000, stock=15),
            Product(name="Keyboard", price=3000, stock=25),
        ])

        db.session.commit()
        print("🌱 Database seeded successfully!")
    else:
        print("✅ Database already exists, skipping seed.")

with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(debug=True, port=5001)
