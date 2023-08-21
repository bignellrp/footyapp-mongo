# Use the official MongoDB image as the base image
FROM mongo:latest

# Set the working directory
WORKDIR /app

# Copy the startup script and data files into the image
COPY startup.py /app/
COPY players.json /app/
COPY games.json /app/

# Run the Python startup script as the entry point
CMD ["python", "/app/startup.py"]