from .database import db
from .models.User import User, RefreshToken
from .models.Equipment import Equipment
from .models.Room import Room


def initialize_database():
    try:
        db.connect()
        print("Database connection opened.")

        db.create_tables([User, RefreshToken, Equipment, Room], safe=True)
        print("Tables created successfully.")

    finally:
        if not db.is_closed():
            db.close()
            print("Database connection closed.")


if __name__ == "__main__":
    initialize_database()
