from .database import db
from .models.User import User, AuthToken


def initialize_database():
    try:
        db.connect()
        print("Database connection opened.")

        db.create_tables([User, AuthToken], safe=True)
        print("Tables created successfully.")

    finally:
        if not db.is_closed():
            db.close()
            print("Database connection closed.")


if __name__ == "__main__":
    initialize_database()
