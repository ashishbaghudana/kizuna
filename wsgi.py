from app import create_app, db
from app.model import User, Contact # Make sure to import your models

app = create_app()

@app.cli.command("reset-db")
def reset_db():
    """Drops and recreates the database tables."""
    db.drop_all()
    db.create_all()
    print("Database has been reset.")