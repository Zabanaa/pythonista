from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from pythonista import app, db
from pythonista.models import Company, Job

migrate = Migrate(app, db, compare_type=True)


manager = Manager(app)

@manager.command
def test():
    from subprocess import call
    call('python -m tests.test', shell=True)

manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
        manager.run()

