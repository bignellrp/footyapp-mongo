#!/bin/bash

# Wait for MongoDB to be ready
while ! nc -z mongodb 27017; do
  sleep 1
done

# Get admin username and password from environment variables
ADMIN_USERNAME="$MONGO_INITDB_ROOT_USERNAME"
ADMIN_PASSWORD="$MONGO_INITDB_ROOT_PASSWORD"

# Set the initial admin username using environment variables
mongo admin --host mongodb --eval "db.createUser({user: '$ADMIN_USERNAME', pwd: '$ADMIN_PASSWORD', roles: [{role: 'root', db: 'admin'}]})"

# Output a message indicating the setup is complete
echo "MongoDB admin user created"