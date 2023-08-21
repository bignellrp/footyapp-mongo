from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access environment variables
#mongo_username = os.getenv("MONGO_INITDB_ROOT_USERNAME")
#mongo_password = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
mongo_username = os.getenv("MONGO_USERNAME")
mongo_password = os.getenv("MONGO_PASSWORD")

# Replace with your MongoDB connection details
mongo_uri = f"mongodb://{mongo_username}:{mongo_password}@localhost:27017/"

try:
    client = MongoClient(mongo_uri)
    db = client['footyapp']
    players_collection = db['players']
    games_collection = db['games']
    print("Connected to MongoDB successfully")
except Exception as e:
    print("Error connecting to MongoDB:", e)

# Routes for Players
@app.route('/players', methods=['GET'])
def get_players():
    players = players_collection.find()
    player_list = [{"_id": str(player["_id"]), "name": player["name"]} for player in players]
    return jsonify(player_list)

@app.route('/players', methods=['POST'])
def add_player():
    new_player = request.json
    player_id = players_collection.insert_one(new_player).inserted_id
    return jsonify({"_id": str(player_id), "message": "Player added successfully"})

# Routes for Games
@app.route('/games', methods=['GET'])
def get_games():
    games = games_collection.find()
    game_list = [{"_id": str(game["_id"]), "date": game["date"]} for game in games]
    return jsonify(game_list)

@app.route('/games', methods=['POST'])
def add_game():
    new_game = request.json
    game_id = games_collection.insert_one(new_game).inserted_id
    return jsonify({"_id": str(game_id), "message": "Game added successfully"})

@app.route('/games/<game_id>', methods=['PUT'])
def update_game(game_id):
    game_updates = request.json
    games_collection.update_one({"_id": ObjectId(game_id)}, {"$set": game_updates})
    return jsonify({"message": "Game updated successfully"})

@app.route('/games/<game_id>', methods=['DELETE'])
def delete_game(game_id):
    games_collection.delete_one({"_id": ObjectId(game_id)})
    return jsonify({"message": "Game deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
