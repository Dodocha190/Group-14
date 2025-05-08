import os
from flask_migrate import upgrade
from app import application, db

DB_PATH = os.path.join("app", "app.db")

def reset_database():
    # Step 1: Remove the existing SQLite database
    if os.path.exists(DB_PATH):
        print(f"Removing existing database at {DB_PATH}...")
        os.remove(DB_PATH)

    # Step 2: Re-apply migrations to create a fresh schema
    with application.app_context():
        upgrade()
        print("Database successfully reset and upgraded.")

if __name__ == "__main__":
    reset_database()
