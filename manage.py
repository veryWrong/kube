from flask_script import Manager, Server
from app import init_app
from app.pods import pod
import os


path = os.path.dirname(os.path.abspath(__file__))
app = init_app()
app.register_blueprint(pod, url_prefix='/pod')
manager = Manager(app)
manager.add_command('server',
                    Server(
                        host='0.0.0.0',
                        port=5050,
                    ))


@manager.shell
def make_shell_context():
    return dict(app=app)


if __name__ == "__main__":
    manager.run()
