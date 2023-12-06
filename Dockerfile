# Use an official Python runtime as a parent image
FROM python:3.11

WORKDIR /app

COPY . /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app/app.py"]


