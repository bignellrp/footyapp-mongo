from flask import Flask
from routes import players, games  # Import routes from the routes folder
app = Flask(__name__)

# Register the routes from the imported route files
app.register_blueprint(players.players_bp)
app.register_blueprint(games.games_bp)

if __name__ == '__main__':
    app.run(debug=True)
