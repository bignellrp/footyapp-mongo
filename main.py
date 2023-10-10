from flask import Flask, request, jsonify
from routes import players, games, tenant  # Import routes from the routes folder
#from flask_jwt_extended import JWTManager # Import JWT for token auth
from dotenv import load_dotenv
import os

##Load the .env file
load_dotenv()

# Create the Flask app
app = Flask(__name__)

# Load JWT envs
#app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
#app.config["JWT_TOKEN_LOCATION"] = ["headers"]

# Run the JWT Manager
#jwt = JWTManager(app)

API_KEYS = {
    "bot": os.getenv("BOT_TOKEN"),
    "web": os.getenv("WEB_TOKEN"),
    "watch": os.getenv("WATCH_TOKEN")
}

def authorize_request(authorization_header):
    # Extract the API key from the authorization header
    provided_api_key = authorization_header.replace("Bearer ", "")

    # Check if the provided API key is in the list of valid API keys
    return provided_api_key in API_KEYS.values()

@app.before_request
def before_request():
    authorization_header = request.headers.get("Authorization")
    if not authorization_header or not authorize_request(authorization_header):
        return jsonify({"message": "Unauthorized"}), 401

# Register the routes from the imported route files
app.register_blueprint(players.players_bp)
app.register_blueprint(games.games_bp)
app.register_blueprint(tenant.tenant_bp)
#app.register_blueprint(login.login_bp)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
