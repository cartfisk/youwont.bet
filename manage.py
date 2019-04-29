import redis
from flask_script import Server, Manager
from rq import Connection, Worker
from wsgi import app


manager = Manager(app)
manager.add_command(
    'runserver',
    Server(port=5000, host="0.0.0.0", use_debugger=True, use_reloader=True))


@manager.command
def runworker():
    redis_url = app.config['REDIS_URL']
    redis_connection = redis.from_url(redis_url)
    with Connection(redis_connection):
        worker = Worker(app.config['QUEUES'])
        worker.work()


if __name__ == '__main__':
    manager.run()
