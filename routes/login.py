# from flask import Blueprint, jsonify, request
# from flask_jwt_extended import create_access_token
# from dotenv import load_dotenv
# import os

# ##Load the .env file
# load_dotenv()

# # Specify the users that can generate tokens
# users = {
#     os.getenv("API_USERNAME") : os.getenv("API_PASSWORD"),
#     # Add more here if needed or use a proper auth mechanism
# }

# # Create the blueprint
# login_bp = Blueprint("login", __name__)

# # Login Route

# @login_bp.route("/login", methods=["POST"])
# def login():
#     data = request.json
#     username = data.get("username") # Get the username from the request header
#     password = data.get("password") # Get the password from the request header
#     # Check if the provided username exists and the password matches
#     if username in users and users[username] == password:
#         # Generate and return a JWT token
#         return jsonify(access_token=create_access_token(username)), 200
#     else:
#         return jsonify({"message": "Invalid username or password"}), 401