# Use an official Python runtime as a base image (os: alpine linux)
FROM python:3.6.1-alpine

# Add requirements.txt before rest of repo, for Docker caching purposes
# See http://ilikestuffblog.com/2014/01/06/
ADD requirements.txt /bot/

# Set the working directory to /bot
WORKDIR bot

# Install any needed packages
RUN pip install -r requirements.txt
RUN apk update && apk add nodejs

# Copy the current directory contents into the container at /bot
ADD . /bot

# We need the PYTHONUNBUFFERED environment variable to
# view the bot's output. If you want to turn it ON, just
# pass 1 when running this image.
ENV PYTHONUNBUFFERED=0

# --- If we are using docker compose, we dont need the settings below ---
# Start the bot
# CMD ["python", "run.py"]
