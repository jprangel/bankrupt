1 - Start the memcached service:

	docker run -p 11211:11211 -it memcached:1.5.11-alpine

2 - Unzip tapps_games and access tapps_games folder;

	unzip tapps_games.zip; cd tapps_games

3 - Create and activate a virtualenv to separate the projects requirements:

	virtualenv -p python3 bankrupt; source bankrupt/bin/activate

4 - Access the bankrupt project and install the requirements via pip:

	cd bankrupt/; pip install -r requirements.txt

5 - Run the script using:

	python src/main.py
