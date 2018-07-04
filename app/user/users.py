from kubernetes import client
from kubernetes.client.rest import ApiException
from flask import jsonify, request, abort
from flask_login import login_user, login_required, logout_user
from sqlalchemy import or_
from app import login_manager
from model.model import User
from manage import db
from utils.utils import check_key
from . import user


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        try:
            user = User.verify_auth_token(api_key)
            return user
        except TypeError:
            pass
    return None


@login_manager.unauthorized_handler
def unauthorized_handler():
    return jsonify({'code': 401, 'msg': '请先登录'})


@user.route('/register', methods=['POST', ])
def register():
    if request.json and request.method == 'POST':
        data = request.get_json()
        email = check_key('email', data)
        if data['username'] is None or data['password'] is None:
            abort(400)
        if User.query.filter_by(username=data['username']).first() is not None:
            abort(400)
        v1 = client.CoreV1Api()
        body = client.V1Namespace()
        body.kind = 'Namespace'
        body.metadata = dict(name=data['username'], lables={
            'name': data['username']
        })
        pretty = 'true'
        try:
            api_response = v1.create_namespace(body, pretty=pretty)
            print(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->create_namespace: %s\n" % e)
            return jsonify({'code': 500, 'msg': '用户已存在'})
        user_data = User(username=data['username'])
        user_data.email = email
        user_data.hash_password(data['password'])
        db.session.add(user_data)
        db.session.commit()
        return jsonify({'code': 200, 'msg': '帐号注册成功'})
    else:
        return jsonify({'code': 500, 'msg': '请求方式错误'})


@user.route('/login', methods=['POST', ])
def login():
    data = request.get_json()
    name = data['username']
    user_data = db.session.query(User).filter(or_(User.email == name, User.username == name)).first()
    if user_data is None:
        return jsonify({'code': 500, 'msg': '用户不存在', 'data': {}})
    if user_data.verify_password(password=data['password']):
        token = user_data.generate_auth_token()
        # remember = check_key('remember', data, False)
        # login_user(user_data, remember)
        return jsonify({
            'code': 200,
            'msg': '登录成功',
            'data': {
                'id': user_data.id,
                'name': user_data.username,
                'email': user_data.email,
                'role': user_data.role,
                'token': token.decode('ascii'),
            }
        })
    else:
        return jsonify({'code': 500, 'msg': '密码错误', 'data': {}})


@user.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'code': 200, 'msg': '退出成功', 'data': {}})


@user.route('/list', methods=['GET', ])
@login_required
def user_list():
    user_data = User.query.all()
    return jsonify({'code': 200, 'msg': 'ok', 'data': [{
        'id': u.id,
        'username': u.username,
        'email': u.email,
        'role': u.role,
        'create_date': u.create_date.strftime("%Y-%m-%d %H:%M:%S"),
    } for u in user_data]})
