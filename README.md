# Comet-web-sensors
STFC-wide project to collect and graph data from Comet T6640 networkable environment monitors. Collects CO2 PPM, temperature, relative humidity and dew point from one or more sensors via HTTP.


## Requirements
- Apache Cassandra data store (https://cassandra.apache.org/download/)
- Python 3.7+
- `python3-cassandra`
- Pip

## Setup
1. Install Apache Cassandra
1. Import schema with `cqlsh --file schema.cql`
1. Create a Python virtual environment (optional but recommended)
1. Install Pip requirements with `pip3 install --requirements requirements.txt`

## Running Data Collection
From a shell, execute `./sensor_data.py`. This runs until terminated.

## Running web UI
From a shell, execute `./server-ui.py`. This starts a Flask server that runs until terminated. The server can be accessed on port 8051 by default.

## Configuration
Edit `config.ini`. Sensors can be added in the `[sensors]` section in the format `IP address: Display name`. Polling interval is configurable (60s by default).



# Docker Image: Comet-web-sensors
Contains three containers:
 - Cassandra Database
 - Sensors data collection
 - Sensors data plot
 

## For Linux usage:

### Install docker
wget -qO- https://get.docker.com/ |sh

### Install docker-compose
pip3 install docker-compose==1.17.1

### Pull required docker images:
sudo docker-compose pull

### Build image:
sudo docker-compose build

### All at once Pull, Build and Run image for the first time
sudo docker-compose up --build -d

### To run all containers:
sudo docker-compose up -d

### Stop all running containers
sudo docker-compose down

### List all running containers
sudo docker ps
Options: -a list all running and stopped containers


## For Windows usage:
  - Install Docker Hub: https://docs.docker.com/docker-for-windows/install/ (restart is needed after installation)
  - If user doesn’t have administrator privileges then it needs to be added to “docker-users” group inside Computer management
  - Using PowerShell:
    - Clone repo: https://github.com/CentralLaserFacility/comet-web-sensor.git
    - Checkout branch: main
    - FILES TO CHANGE BEFORE BUILD:
      - data_plot/DAO.py: Connect to DB container in Line 33: 
                            - self.cluster = Cluster(["cassandra_db"],protocol_version=4)
    - Build and run doker containers: docker-compose -f docker-compose-windows.yml up –d --build  (this will take a few minutes)
    - To initialize the database (Only needs to be done once)
      - docker exec -it cassandra_db sh
      - cqlsh --file schema.cql 
      - exit 

## If Cassandra is installed locally:
  - Comment the following blocks in docker-compose.yml file:
    - db
    - depends_on: all
