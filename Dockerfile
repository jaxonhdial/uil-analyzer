# 1. Base image: Python installed already (Starts from Linux image that has Python)
FROM python:3.12-slim

# 2. Set Working Directory inside the container (like cd /app)
WORKDIR /app

# 3. Copy dependency list first (for caching) (copies file from local machine into image)
COPY requirements.txt .

# 4. Install Python Dependencies (Executes commands at build time)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your project
COPY . .

# Volumes: Ensures directory exists for SQLite DB
RUN mkdir -p /app/backend/database

# 6. Expose Flask's Port
EXPOSE 5000

#7. Run your Flask App (Command that runs when the container starts)
CMD ["python3", "-m", "backend.server"]