#Update system
sudo apt update

#Install docker
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io

#Change docker deamon ip
sudo sh -c "echo '{
  \"bip\": \"172.26.0.1/16\"
}' > /etc/docker/daemon.json"

sudo systemctl restart docker

#Create the docker group in case it doesn't exist
sudo groupadd docker

#Add current user to "docker" group
sudo usermod -aG docker $USER

#Install docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

#Create data folders for databases (Used in docker volumes)
mkdir -p ~/database/relational/data
mkdir -p ~/database/time_series/data
