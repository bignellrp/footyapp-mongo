from flask import Flask, request, jsonify
from pymongo import MongoClient, ASCENDING
from bson import ObjectId
import json

app = Flask(__name__)

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access environment variables
# Init script might not be working as mongo nonroot user is not working
mongo_username = os.getenv("MONGO_INITDB_ROOT_USERNAME")
mongo_password = os.getenv("MONGO_INITDB_ROOT_PASSWORD")

# Replace with your MongoDB connection details
# How can i get the mongo IP as a variable
mongo_uri = f"mongodb://{mongo_username}:{mongo_password}@172.20.0.2:27017/"

try:
    client = MongoClient(mongo_uri)
    db = client['footyapp']
    players_collection = db['players']
    games_collection = db['games']

    # Create a unique index on the 'name' field
    db.players.create_index([("name", ASCENDING)], unique=True)
    # Create a unique index on the 'name' field
    db.games.create_index([("date", ASCENDING)], unique=True)

    print("Database connection successfull!")

    try:
        # Insert player data from players.json
        with open('players.json', 'r') as players_file:
            players_data = json.load(players_file)
            players_collection.insert_many(players_data)

        # Insert game data from games.json
        with open('games.json', 'r') as games_file:
            games_data = json.load(games_file)
            games_collection.insert_one(games_data)
    except Exception as e:
        print("Duplicate data detected:", e)

except Exception as e:
    print("Error connecting to MongoDB:", e)

# Routes for Players
@app.route('/players', methods=['GET'])
def get_players():
    players = players_collection.find()
    player_list =   [   {
                            "name": player["name"],
                            "total": player["total"],
                            "wins": player["wins"],
                            "draws": player["draws"],
                            "losses": player["losses"],
                            "score": player["score"],
                            "playing": player["playing"],
                            "played": player["played"],
                            "percent": player["percent"],
                            "winpercent": player["winpercent"]
                        } 
                    for player in players
                    ]
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

@app.route('/games/<date>', methods=['PUT'])
def update_game(date):
    game_updates = request.json
    games_collection.update_one({"date": date}, {"$set": game_updates})
    return jsonify({"message": "Game updated successfully"})

@app.route('/games/<date>', methods=['DELETE'])
def delete_game(date):
    games_collection.delete_one({"date": date})
    return jsonify({"message": "Game deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
