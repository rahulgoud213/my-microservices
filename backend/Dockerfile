FROM python:3.9-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1

# Install Python dependencies. Copy only requirements first for better layer caching.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the Flask app will run on
EXPOSE 5001

CMD ["python", "app.py"]