from pymongo import MongoClient, ASCENDING
import json
from dotenv import load_dotenv
import os

def db_connect():
    try:
        # Load environment variables from .env file
        load_dotenv()

        # Access environment variables
        # Init script might not be working as mongo nonroot user is not working
        mongo_username = os.getenv("MONGO_INITDB_ROOT_USERNAME")
        mongo_password = os.getenv("MONGO_INITDB_ROOT_PASSWORD")

        # Replace with your MongoDB connection details
        # How can i get the mongo IP as a variable
        mongo_uri = f"mongodb://{mongo_username}:{mongo_password}@172.20.0.2:27017/"

        # Connect to MongoDB
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
        
    return players_collection, games_collection