# Result-aggregation-server

Result aggregation server is a flask api and server that will be used to store the results returned by [installation test scripts](https://github.com/wking/swc-setup-installation-test). Currently the results are not being stored and thus no useful information is being extracted out of it.
This server will enable instructors to identify the most faulty packages and versions and would help the [Software carpentry](http://software-carpentry.org/) students in the installation proccess.

To fly this aircraft:

* Clone this repository
```
git clone git@github.com:prerit2010/Result-aggregation-server.git
```
* Project is built on python3

* Create a Virtual environment
```
cd Result-aggregation-server
virtualenv -p python3 env
```
* Activate Virtual Environment
```
source env/bin/activate
```
* Install dependencies
```
pip install -r requirements.txt`
```
* One other dependency is Redis, which is used for throttling:
```
sudo apt-get install redis-server
```

* Perform flask migrations

Run the following command just once to initiate the migrations.
```
python manage.py db init
```
Everytime there are some schematic changes in the database, run the following 2 commands :

```
python manage.py db migrate
python manage.py db upgrade
```

* If you want to add a sample database for testing :
```
python manage.py import_db
```

* Test the API:

```
python test.py
```
* Run :

```
python run.py
```