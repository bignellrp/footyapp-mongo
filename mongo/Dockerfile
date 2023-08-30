FROM mongo:latest

# Copy the init-mongo.sh script into the container
COPY init-mongo.sh /docker-entrypoint-initdb.d/init-mongo.sh

# Set the script as executable
RUN chmod +x /docker-entrypoint-initdb.d/init-mongo.sh

# Start MongoDB using the original entrypoint script
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["mongod"]