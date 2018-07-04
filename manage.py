from flask_script import Manager, Server
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from app import init_app
from app.deploy import deploy
from app.pods import pod
from app.user import user
from app.nodes import node


app = init_app()
app.register_blueprint(pod, url_prefix='/pod')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(node, url_prefix='/node')
app.register_blueprint(deploy, url_prefix='/deploy')
db = SQLAlchemy(app)

from model.model import *
manager = Manager(app)
manager.add_command('server',
                    Server(
                        host='0.0.0.0',
                        port=5050,
                    ))


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, datetime=datetime, User=User)


@app.route('/', methods=['GET', ])
def index():
    return jsonify({'code': 200, 'msg': '项目启动成功', 'data': []})


if __name__ == "__main__":
    manager.run()
