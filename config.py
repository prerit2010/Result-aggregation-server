from os.path import expanduser
home = expanduser("~")
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + home + '/result_aggregation.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False