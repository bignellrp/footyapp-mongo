FROM mongo:latest

# Define build arguments with default values
ARG MONGO_INITDB_ROOT_USERNAME
ARG MONGO_INITDB_ROOT_PASSWORD
ARG MONGO_USERNAME
ARG MONGO_PASSWORD

# Copy the startup script and data files into the image
COPY startup.sh /tmp/
COPY players.json /tmp/
COPY games.json /tmp/

# Make the script executable
RUN chmod +x /tmp/startup.sh

# Pass build arguments as environment variables during the build process
ENV MONGO_INITDB_ROOT_USERNAME=$MONGO_INITDB_ROOT_USERNAME
ENV MONGO_INITDB_ROOT_PASSWORD=$MONGO_INITDB_ROOT_PASSWORD
ENV MONGO_USERNAME=$MONGO_USERNAME
ENV MONGO_PASSWORD=$MONGO_PASSWORD

# Run the Bash script as the entry point
CMD ["bash", "/tmp/startup.sh"]