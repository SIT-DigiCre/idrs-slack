# Python 3.7 image on Debian stretch for ARMv7
FROM arm32v7/python:3.7-stretch

# Install pipenv
RUN pip install pipenv
# Set PIPENV_TIMEOUT=1000 to prevent timeout err
ENV PIPENV_TIMEOUT 1000

# Install image libraries
RUN apt-get update && apt-get install -y libjpeg-dev zlib1g-dev

# Setup pipenv
COPY Pipfile ./
COPY Pipfile.lock ./
RUN pipenv install --system
RUN rm Pipfile Pipfile.lock
