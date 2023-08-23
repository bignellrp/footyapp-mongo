from flask import Blueprint, jsonify, request
from db_connect import db_connect

games_bp = Blueprint("games", __name__)
players_collection, games_collection = db_connect()

# Routes for Games
@games_bp.route('/games', methods=['GET'])
def get_games():
    games = games_collection.find()
    game_list = [{"_id": str(game["_id"]), "date": game["date"]} for game in games]
    return jsonify(game_list)

@games_bp.route('/games', methods=['POST'])
def add_game():
    new_game = request.json
    game_id = games_collection.insert_one(new_game).inserted_id
    return jsonify({"_id": str(game_id), "message": "Game added successfully"})

@games_bp.route('/games/<date>', methods=['PUT'])
def update_game(date):
    game_updates = request.json
    games_collection.update_one({"date": date}, {"$set": game_updates})
    return jsonify({"message": "Game updated successfully"})

@games_bp.route('/games/<date>', methods=['DELETE'])
def delete_game(date):
    games_collection.delete_one({"date": date})
    return jsonify({"message": "Game deleted successfully"})