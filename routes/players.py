from flask import Blueprint, jsonify, request
from db_connect import db_connect

players_bp = Blueprint("players", __name__)
players_collection, games_collection = db_connect()

# Routes for Players
@players_bp.route('/players', methods=['GET'])
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

@players_bp.route('/players', methods=['POST'])
def add_player():
    new_player = request.json
    player_id = players_collection.insert_one(new_player).inserted_id
    return jsonify({"_id": str(player_id), "message": "Player added successfully"})