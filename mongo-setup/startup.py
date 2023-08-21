from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json

# Load environment variables from .env file
load_dotenv()

# Access environment variables
mongo_root_username = os.getenv("MONGO_INITDB_ROOT_USERNAME")
mongo_root_password = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
mongo_username = os.getenv("MONGO_USERNAME")
mongo_password = os.getenv("MONGO_PASSWORD")

# Replace with your MongoDB connection details
mongo_uri = f"mongodb://{mongo_username}:{mongo_password}@localhost:27017/"

try:
    # Connect to MongoDB
    client = MongoClient(mongo_uri)
    admin_db = client.admin

    # Create players and games databases
    players_db = client.players
    games_db = client.games

    # Create users in players and games databases
    player_user = {
        "user": {mongo_username},
        "pwd": {mongo_password},
        "roles": [{"role": "readWrite", "db": "players"}]
    }
    players_db.command("createUser", **player_user)

    game_user = {
        "user": {mongo_username},
        "pwd": {mongo_password},
        "roles": [{"role": "readWrite", "db": "games"}]
    }
    games_db.command("createUser", **game_user)

    # Insert player data from players.json
    with open('players.json', 'r') as players_file:
        players_data = json.load(players_file)
        players_collection = players_db.players
        players_collection.insert_many(players_data)

    # Insert game data from games.json
    with open('games.json', 'r') as games_file:
        games_data = json.load(games_file)
        games_collection = games_db.games
        games_collection.insert_many(games_data)

    print("Databases, users, and data inserted successfully")

except Exception as e:
    print("Error:", e)

finally:
    # Close the MongoDB connection
    client.close()