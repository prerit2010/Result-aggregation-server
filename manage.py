from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from config import SAMPLE_DATABASE_URI
from app import application, db
import sqlite3
 
migrate = Migrate(application, db)
 
manager = Manager(application)
manager.add_command('db', MigrateCommand)

@manager.command
def import_db():
    print("\nImporting sample data....\n")
    try:
        con = sqlite3.connect(SAMPLE_DATABASE_URI)
        f = open('sample.sql', 'r')
        sql = f.read()
        con.executescript(sql)
        con.close()
    except:
        print("Could not connect to database")
    else:
        print("Sample data imported successfully")
 
if __name__ == '__main__':
    manager.run()