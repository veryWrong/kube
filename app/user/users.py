from kubernetes import client
from kubernetes.client.rest import ApiException
from flask import jsonify, request, abort
from sqlalchemy import or_
from model.model import User
from manage import db
from utils.utils import check_key
from . import user


@user.route('/register', methods=['POST', ])
def register():
    if request.json and request.method == 'POST':
        # username = request.json['username']
        # password = request.json['password']
        # email = request.json['email']
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
        return jsonify({'code': 500, 'msg': '密码错误', 'data': {}})
    if user_data.verify_password(password=data['password']):
        return jsonify({
            'code': 200,
            'msg': '登录成功',
            'data': {
                'id': user_data.id,
                'name': user_data.username,
                'email': user_data.email,
                'role': user_data.role,
            }
        })
    else:
        return jsonify({'code': 500, 'msg': '密码错误', 'data': {}})
