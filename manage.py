from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from config import SAMPLE_DATABASE_URI
from app import application, db
import sqlite3, sys
 
migrate = Migrate(application, db)
 
manager = Manager(application)
manager.add_command('db', MigrateCommand)

@manager.command
def import_db():
    tables = ['user_system_info', 'successful_installs', 'failed_installs' ,'attempts']
    try:
        con = sqlite3.connect(SAMPLE_DATABASE_URI)
    except:
        print("\nCould not connect to database")
        sys.exit(0)
    cursor = con.execute("SELECT * from user_system_info limit 1")
    result= cursor.fetchone()
    if result:
        choice = input("Database already contains some data. Do you wish to delete all data and overwrite? (y/n) :")
        if choice == 'y' or choice == 'Y':
            for table in tables:
                con.execute("DELETE FROM " + table)
        else:
            sys.exit(0)
    print("\nImporting sample data....\n")
    with open('sample.sql', 'r') as f:
        sql = f.read()
    con.executescript(sql)
    con.close()
    print("\nSample data imported successfully")
 
if __name__ == '__main__':
    manager.run()