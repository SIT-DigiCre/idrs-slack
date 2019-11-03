# Python 3.5 image on Debian stretch for ARMv7
FROM python:3.5-buster

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
