from os.path import expanduser
home = expanduser("~")
SAMPLE_DATABASE_URI = home + '/result_aggregation.db'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + home + '/result_aggregation.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False