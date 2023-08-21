#!/bin/bash

# Load environment variables from .env file
source ../.env

# Replace with your MongoDB connection details
mongo_uri="mongodb://${MONGO_USERNAME}:${MONGO_PASSWORD}@localhost:27017/"

# Create users in players and games databases
mongo <<EOF
use players
db.createUser({
    user: "${MONGO_USERNAME}",
    pwd: "${MONGO_PASSWORD}",
    roles: [{ role: "readWrite", db: "players" }]
});
EOF

mongo <<EOF
use games
db.createUser({
    user: "${MONGO_USERNAME}",
    pwd: "${MONGO_PASSWORD}",
    roles: [{ role: "readWrite", db: "games" }]
});
EOF

# Insert player data from players.json
mongoimport --uri="${mongo_uri}players" --collection=players --file=players.json --jsonArray

# Insert game data from games.json
mongoimport --uri="${mongo_uri}games" --collection=games --file=games.json --jsonArray

echo "Databases, users, and data inserted successfully"