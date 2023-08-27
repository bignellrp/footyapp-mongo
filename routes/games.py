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

@games_bp.route('/games/wins/<player>', methods=['GET'])
@jwt_required()
def get_game_wins(player):
    # Count games that match the criteria
    count = games_collection.count_documents({
        "scoreTeamA": {"$gt": "scoreTeamB"},
        "teamA": {"$elemMatch": {"$in": [player]}}
    })
    
    # Update the number of wins for the player
    players_collection.update_one({"name": player},{"$inc": {"wins": 1}})
    
    return jsonify({"wins": count})

@games_bp.route('/games/updatescore/<date>', methods=['PUT'])
@jwt_required()
def update_score(date):
    game = games_collection.find_one({"date": date})
    if game:
        game["date"] = datetime.strptime(game["date"], '%Y-%m-%d')
        game_record = {
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
    score = request.json
    games_collection.update_one({"date": date}, {"$set": score})
    if score["scoreTeamA"] > score["scoreTeamB"]:
        print("Team A Won! Updating stats.")
        for player in game_record["teamA"]:
            players_collection.update_one({"name": player},{"$inc": {"wins": 1}})
            players_collection.update_one({"name": player},{"$inc": {"played": 1}})
            players_collection.update_one({"name": player},{"$inc": {"score": 3}})
        for player in game_record["teamB"]:
            players_collection.update_one({"name": player},{"$inc": {"losses": 1}})
            players_collection.update_one({"name": player},{"$inc": {"played": 1}})
    elif score["scoreTeamA"] < score["scoreTeamB"]:
        print("Team B Won! Updating stats.")
        for player in game_record["teamB"]:
            players_collection.update_one({"name": player},{"$inc": {"wins": 1}})
            players_collection.update_one({"name": player},{"$inc": {"played": 1}})
            players_collection.update_one({"name": player},{"$inc": {"score": 3}})
        for player in game_record["teamA"]:
            players_collection.update_one({"name": player},{"$inc": {"losses": 1}})
            players_collection.update_one({"name": player},{"$inc": {"played": 1}})
    elif score["scoreTeamA"] == score["scoreTeamB"]:
        print("Draw! Updating stats.")
        for player in game_record["teamB"]:
            players_collection.update_one({"name": player},{"$inc": {"draws": 1}})
            players_collection.update_one({"name": player},{"$inc": {"played": 1}})
            players_collection.update_one({"name": player},{"$inc": {"score": 1}})
        for player in game_record["teamA"]:
            players_collection.update_one({"name": player},{"$inc": {"draws": 1}})
            players_collection.update_one({"name": player},{"$inc": {"played": 1}})
            players_collection.update_one({"name": player},{"$inc": {"score": 1}})
    #Need to make sure the player_collection is updated by the above first
    for player in game_record["teamA"] or game_record["teamB"]:
        findplayer = players_collection.find_one({"name": player})
        if findplayer:
            player_record = {
                "name": findplayer["name"],
                "total": findplayer["total"],
                "wins": findplayer["wins"],
                "draws": findplayer["draws"],
                "losses": findplayer["losses"],
                "score": findplayer["score"],
                "playing": findplayer["playing"],
                "played": findplayer["played"],
                "percent": findplayer["percent"],
                "winpercent": findplayer["winpercent"]
            }
        percentage = player_record["wins"] / player_record["played"] * 100
        if player_record["wins"] < 5:
            winpercentage = '0'
        else:
            winpercentage = percentage
        players_collection.update_one({"name": player},{"$set": {"percent": percentage}})
        players_collection.update_one({"name": player},{"$inc": {"winpercent": winpercentage}})
    return jsonify({"message": "Game updated successfully"})

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