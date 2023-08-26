from flask import Flask
from routes import players, games, login  # Import routes from the routes folder
from flask_jwt_extended import JWTManager # Import JWT for token auth
from dotenv import load_dotenv
import os

##Load the .env file
load_dotenv()

# Create the Flask app
app = Flask(__name__)

# Load JWT envs
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_TOKEN_LOCATION"] = ["headers"]

# Run the JWT Manager
jwt = JWTManager(app)

# Register the routes from the imported route files
app.register_blueprint(players.players_bp)
app.register_blueprint(games.games_bp)
app.register_blueprint(login.login_bp)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
