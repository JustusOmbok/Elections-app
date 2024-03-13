from flask import Flask
from flask.cli import FlaskGroup
from flask_migrate import Migrate, MigrateCommand
from app import app, db

app = Flask(__name__)
#app.config.from_object("config.Config")

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Create a custom FlaskGroup
cli = FlaskGroup(app)

# Add Flask-Migrate commands to the Flask CLI
cli.add_command("db", MigrateCommand)

if __name__ == "__main__":
    cli()