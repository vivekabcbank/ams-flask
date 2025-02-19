# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app/

# Expose the port for the Flask app
EXPOSE 5000

# Run Gunicorn server
CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]
