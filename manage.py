# manage.py

import unittest
import coverage

from flask_script import Manager
from flask_migrate import MigrateCommand

from project import app, db, celery
from project.api.models import User

COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*'
    ]
)
COV.start()

manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    """Runs the tests without code coverage."""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@manager.command
def recreate_db():
    """Recreates a database."""
    db.drop_all()
    db.create_all()
    db.session.commit()

@manager.command
def seed_db():
    """Seeds the database."""
    db.session.add(User(username='martin', email="mtn.barreto@gmail.com", password="password"))
    db.session.add(User(username='barreto', email="barretomartin1984@gmail.com", password="password"))
    db.session.commit()

@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1

@manager.command
def local_env_vars():
    print("export APP_SETTINGS=project.config.DevelopmentConfig")
    print("export SECRET_KEY='mysecret'")
    print("export DATABASE_TEST_URL='postgres://postgres:postgres@localhost:5432/flask_base_test'")
    print("export DATABASE_URL='postgres://postgres:postgres@localhost:5432/flask_base_dev'")
    print("export CELERY_BROKER_URL='amqp://'")
    print("export CELERY_RESULT_BACKEND='rpc://'")

if __name__ == '__main__':
    manager.run()
