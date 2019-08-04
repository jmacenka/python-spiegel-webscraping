sudo docker rm -f $(sudo docker ps -aq)
sudo docker build -t webscraping:latest .
sudo docker volume create webscraping
sudo docker run -d --name webscraping -v webscraping:/app/spiegel_artikel/ webscraping
