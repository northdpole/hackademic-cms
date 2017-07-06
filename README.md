# hackademic-cms
hackademic-cms
THe project is written in python3
The project runs in a virtual environment for development purposes.
All contributions should come with unit tests whith as much coverage as possible.
In order to setup the virtual environment you can execute

virtualenv v
source v/bin/activate
pip install -r requirements.txt

# Testing:
from within the virtual environment run python manage.py test hcapp
with coverage you can use the coverage module installed


#rUNNING THE SERVER
first you need to do the migrations

python manage.py makemigrations hcapp

then migrate
python manage.py migrate

then
python manage.py runserver 
