from flask import Blueprint, jsonify, request
from db_connect import db_connect
from datetime import datetime
from flask_jwt_extended import jwt_required


games_bp = Blueprint("games", __name__)
players_collection, games_collection = db_connect()

# Routes for Games
@games_bp.route('/games', methods=['GET'])
@jwt_required()
def get_games():
    games = games_collection.find()
    # for game in games:
    #         game["date"] = datetime.strptime(game["date"], '%Y-%m-%d')
    game_list =   [   {
                            "date": game["date"],
                            "teamA": [game["teamA"]],
                            "teamB": [game["teamB"]],
                            "scoreTeamA": game["scoreTeamA"],
                            "scoreTeamB": game["scoreTeamB"],
                            "totalTeamA": game["totalTeamA"],
                            "totalTeamB": game["totalTeamB"],
                            "colourTeamA": game["colourTeamA"],
                            "colourTeamB": game["colourTeamB"]
                        } 
                    for game in games
                    ]
    return jsonify(game_list)

@games_bp.route('/games/game_stats', methods=['GET'])
@jwt_required()
def get_game_stats():
    games = list(games_collection.find())  # Convert cursor to a list
    for game in games:
        game["date"] = datetime.strptime(game["date"], '%Y-%m-%d')

    # Sort players by name in alphabetical order
    # This might not work until date is converted in the api
    sorted_games = sorted(games, key=lambda game: game["date"], reverse=True)
    game_list =   [   {
                            "date": game["date"].strftime('%Y-%m-%d'),
                            "scoreTeamA": game["scoreTeamA"],
                            "scoreTeamB": game["scoreTeamB"]
                        } 
                    for game in sorted_games
                    ]
    return jsonify(game_list)

@games_bp.route('/games/most_recent_game', methods=['GET'])
@jwt_required()
def get_most_recent_game():
    games = list(games_collection.find())  # Convert cursor to a list
    for game in games:
        game["date"] = datetime.strptime(game["date"], '%Y-%m-%d')

    # Sort players by name in alphabetical order
    # This might not work until date is converted in the api
    sorted_games = sorted(games, key=lambda game: game["date"], reverse=True)
    game_list =   [   {
                            "date": game["date"].strftime('%Y-%m-%d'),
                            "teamA": game["teamA"],
                            "teamB": game["teamB"],
                            "scoreTeamA": game["scoreTeamA"],
                            "scoreTeamB": game["scoreTeamB"],
                            "totalTeamA": game["totalTeamA"],
                            "totalTeamB": game["totalTeamB"],
                            "colourTeamA": game["colourTeamA"],
                            "colourTeamB": game["colourTeamB"]
                        } 
                    for game in sorted_games
                    ]
    return jsonify(game_list)

@games_bp.route('/games', methods=['POST'])
@jwt_required()
def add_game():
    new_game = request.json
    game_id = games_collection.insert_one(new_game).inserted_id
    return jsonify({"_id": str(game_id), "message": "Game added successfully"})

@games_bp.route('/games/<date>', methods=['PUT'])
@jwt_required()
def update_game(date):
    game_updates = request.json
    games_collection.update_one({"date": date}, {"$set": game_updates})
    return jsonify({"message": "Game updated successfully"})

@games_bp.route('/games/<date>', methods=['DELETE'])
@jwt_required()
def delete_game(date):
    games_collection.delete_one({"date": date})
    return jsonify({"message": "Game deleted successfully"})