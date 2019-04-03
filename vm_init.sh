#Update system
sudo apt update

#Install docker
sudo apt install docker.io

#Add current user to "docker" group
sudo usermod -aG docker $USER

#Install docker-compose
sudo apt install docker-compose

#Create data folders for databases (Used in docker volumes)
mkdir -p ~/database/relational/data
mkdir -p ~/database/time_series/data
