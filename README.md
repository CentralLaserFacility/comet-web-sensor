# Docker Image: Comet-web-sensors
Docker image contains three containers:
 - Cassandra Database
 - Sensors data collection
 - Sensors data plot
 

# Installation on Linux:

# Install docker
wget -qO- https://get.docker.com/ |sh

# Install docker-compose
pip3 install docker-compose==1.17.1

# Pull required docker images:
sudo docker-compose pull

# Build image:
sudo docker-compose build

# All at once Pull, Build and Run image for the first time
sudo docker-compose up --build -d

# To run all containers:
sudo docker-compose up -d

# Stop all running containers
sudo docker-compose down

# List all running containers
sudo docker ps
Options: -a list all running and stopped containers
