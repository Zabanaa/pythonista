from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from pythonista import app, db
from pythonista.models import Company, Job

migrate = Migrate(app, db, compare_type=True) 
manager = Manager(app)


@manager.command
def test():
    '''
        This function will enable the user to run the tests by issuing a single
        command:
        python manage.py test
    '''
    from subprocess import call
    call('python -m tests.test', shell=True)

# This adds the db command to our module
# We can then do python manage.py db init/migrate/upgrade etc
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
        manager.run()

