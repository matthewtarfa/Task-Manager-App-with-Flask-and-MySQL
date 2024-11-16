FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install wait-for-it tool
RUN apt-get update && apt-get install -y wait-for-it

# Copy the application code
COPY . .

# Use wait-for-it to wait for DB and start the Flask app
CMD ["wait-for-it", "db:3306", "--", "python", "app.py"]


