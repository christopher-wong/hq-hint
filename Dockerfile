# Use an official Python runtime as a parent image
FROM python:3.6-slim

LABEL name="Christopher Wong"
LABEL email="cwong@christopherwong.co"

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Download NLTK data
RUN [ "python", "-c", "import nltk; nltk.download('all')" ]

# Run entrypoint
CMD ["python", "hq_main.py"]