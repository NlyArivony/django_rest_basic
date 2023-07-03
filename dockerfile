# Use an official Python runtime as the base image
FROM python:3.9-alpine3.13

# Set the working directory in the container
WORKDIR /app

# Copy the project code to the container
COPY . .

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Apply database migrations
RUN python manage.py migrate

# Expose the port that Django runs on
EXPOSE 8000

# Set the default command to run when starting the container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]