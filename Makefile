
install-dependencies:
	sudo apt-get install python3-pip
	sudo apt-get install postgresql postgresql-contrib uwsgi
	pip3 install --upgrade pip
	pip3 install -r requirements.txt