# Using the official Python image
FROM python:3.9-slim

# Setting up the working directory
WORKDIR /usr/src/app

# Copy the project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the script
CMD ["python", "parser_chat.py"]
