# Result-aggregation-server

Result aggregation server is a flask api and server that will be used to store the results returned by [installation test scripts](https://github.com/wking/swc-setup-installation-test). Currently the results are not being stored and thus no useful information is being extracted out of it.
This server will enable instructors to identify the most faulty packages and versions and would help the [Software carpentry](http://software-carpentry.org/) students in the installation proccess.

To fly this aircraft:

* Clone this repository
```
git clone git@github.com:prerit2010/Result-aggregation-server.git
```

* create a Virtual environment
```
cd Result-aggregation-server
virtualenv env
```
* Activate Virtual Environment
```
source env/bin/activate
```
* Install dependencies
```
pip install -r requirements.txt`
```
* Perform flask migrations
```
python manage.py db migrate
python manage.py db upgrade
```
* Run
`python run.py`