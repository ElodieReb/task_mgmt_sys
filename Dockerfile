# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Set the working directory to the root of your application
WORKDIR /task_mgmt_sys

# Copy the content of the local src directory to the working directory
COPY . .

# Creates a non-root user with an explicit UID and adds permission to access the working directory
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /task_mgmt_sys
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
