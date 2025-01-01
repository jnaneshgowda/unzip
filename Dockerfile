# Use Python base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port for Koyeb
EXPOSE 8000

# Start the bot
CMD ["python", "bot.py"]
