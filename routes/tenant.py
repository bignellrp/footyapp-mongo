from flask import Blueprint, jsonify, request
from db_connect import db_connect
#from flask_jwt_extended import jwt_required

# Create the blueprint
tenant_bp = Blueprint("tenant", __name__)

# Connect to the database
players_collection, games_collection, tenant_collection = db_connect()

# Routes for Tenant

@tenant_bp.route('/tenant', methods=['GET'])
#@jwt_required()
def get_tenant_info():
    tenants = tenant_collection.find()
    tenant_list =   [   {
                            "teamname": tenant["teamname"],
                            "channelid": tenant["channelid"],
                            "playernum": tenant["playernum"]
                        } 
                    for tenant in tenants
                    ]
    return jsonify(tenant_list)

@tenant_bp.route('/tenant/<teamname>', methods=['PUT'])
#@jwt_required()
def update_playernum(teamname):
    updated_data = request.json  # New values to update for the specific tenant

    # Update the specific player by matching the unique identifier
    result = tenant_collection.update_one({"teamname": teamname}, {"$set": updated_data})

    if result.modified_count > 0:
        return jsonify({"message": "Tenant updated successfully"})
    else:
        return jsonify({"message": "Tenant not found or no changes applied"})