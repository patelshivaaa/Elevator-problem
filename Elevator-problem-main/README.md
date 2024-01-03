# Elevator-problem

The elevator system is built completely from the user perspective. There are elevator systems(Equivalent to buildings) that contains some elevators. Now some user comes in and makes a request to an elevator. The elevator automatically moves UP/DOWN as per the request of the user.The elevator's algorithm to process the requests can be optimized further. The status of an elevator like it is currently operational or not can be updated using API calls. Visit the [DOCS.md](https://github.com/patelshivaaa/eva) for further information.

## Installation : 
1. Make a python virtual enviornment in your preferred Linux/WSL2...any system
```
Recommended python version -----> 3.8.X (The LATEST STABLE RELEASE)
Some of the packages are not up-to date with python 3.9 or 3.10
```

2. Clone the repo and navigate to the directory where the manage.py file is located
```
git clone https://github.com/patelshivaaa/eva
```
```
cd Elevator-problem
```

3. Please read the special note point number 2 below, and go through the entire notes once.

4. Install the requirements
```
pip install -r requirements.txt
```
5. Run the development server
```
python manage.py runserver
```

## Special Note :

1. The code is repeatative in some cases as I have used each view only for one type of HTTP Method to provide a better understanding.

2. Redis caching is done for the entire site with a time limit of 5 minutes, so if you update the DB the changes in a cached device will appear 5 minutes later.

3. Please make sure redis is installed and running in your device. If it is running in a different port than 6379 then please go to [Elevator/Settings.py](https://github.com/patelshivaaa/eva/blob/main/Elevator/settings.py) and update it at line number : 158.

4. The elevator is running in a different thread and processes all the requests immediately. Check [core/move_elevator.py](https://github.com/patelshivaaa/eva/blob/main/core/move_elevator.py) and [core/apps.py](https://github.com/patelshivaaa/eva/blob/main/core/apps.py) to know more details.

5. sqlite3 DB is used for portability in GitHub. Postgres code is also given below you can replace it at [Elevator/settings.py-line-95](https://github.com/patelshivaaa/eva/blob/main/Elevator/settings.py#L95).
```
DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': ‘<database_name>’,
       'USER': '<database_username>',
       'PASSWORD': '<password>',
       'HOST': '<database_hostname_or_ip>',
       'PORT': '<database_port>',
   }
}
```

4. Please check the models representation and API endpoints at [DOCS.md](https://github.com/patelshivaaa/eva/blob/main/DOCS.md)

5. Please share the scope of improvements you are able to see.
