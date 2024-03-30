# Usage
# docker build -t pleuzhaw/bookingscraper .
# docker run --name bookingscraper -e AZURE_STORAGE_CONNECTION_STRING='***' -p 9001:80 -d pleuzhaw/bookingscraper

FROM python:3.12.1

# Copy Files
WORKDIR /usr/src/app
COPY service.py service.py
COPY templates/index.html templates/index.html

# Install
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Docker Run Command
EXPOSE 80
ENV FLASK_APP=/usr/src/app/service.py
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0", "--port=80"]