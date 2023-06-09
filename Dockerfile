# Use an official Python runtime as a parent image
FROM python:3.9-alpine

# Set the working directory to /usr/elevateai
WORKDIR /usr/elevateai

# Copy the current directory contents into the container at /usr/elevateai
COPY . /usr/elevateai

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py", "-d", "input"]

