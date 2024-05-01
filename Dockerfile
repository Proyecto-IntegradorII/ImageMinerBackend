# Use an official Python runtime as a parent image
FROM python:3.9-slim










# Use the official Selenium base image with standalone Chrome and Firefox
FROM selenium/standalone-chrome:latest as chrome
FROM selenium/standalone-firefox:latest as firefox

# Install Python and pip
USER root
RUN apt-get update && apt-get install -y python3 python3-pip
# Install system dependencies
# Install Python and pip
USER root
RUN apt-get update -qq -y && \
    apt-get install -y \
        libasound2 \
        libatk-bridge2.0-0 \
        libgtk-4-1 \
        libnss3 \
        xdg-utils \
        wget && \
    wget -q -O chrome-linux64.zip https://bit.ly/chrome-linux64-121-0-6167-85 && \
    unzip chrome-linux64.zip && \
    rm chrome-linux64.zip && \
    mv chrome-linux64 /opt/chrome/ && \
    ln -s /opt/chrome/chrome /usr/local/bin/ && \
    wget -q -O chromedriver-linux64.zip https://bit.ly/chromedriver-linux64-121-0-6167-85 && \
    unzip -j chromedriver-linux64.zip chromedriver-linux64/chromedriver && \
    rm chromedriver-linux64.zip && \
    mv chromedriver /usr/local/bin/



    
# Install Python dependencies
# Install Python and pip
USER root
RUN pip install --no-cache-dir Flask==2.2.5 selenium==4.20.0 flask_cors webdriver-manager google-api-python-client google-auth-httplib2 google-auth-oauthlib waitress


WORKDIR /code
COPY . /code




RUN pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
RUN pip install Flask==2.2.5 selenium==4.20.0 flask_cors
RUN pip install waitress
RUN pip install webdriver-manager
EXPOSE 5000
# Start the FastAPI application
CMD ["python3", "main.py", "--host", "0.0.0.0", "--port", "5000", "--reload"]