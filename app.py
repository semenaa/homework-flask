from hashlib import md5
from typing import Type

from flask import Flask, jsonify, request
from flask.views import MethodView
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from models import Session, User
from schema import CreateUser, UpdateUser

app = Flask(__name__)

SALT = '12345'


def hash_password(password: str):
    password = f'{SALT}{password}'
    password = password.encode()
    return md5(password).hexdigest()


class HttpError(Exception):
    def __init__(self, status_code: int, error_message: dict | list | str):
        self.status_code = status_code
        self.error_message = error_message


def validate(schema: Type[CreateUser] | Type[UpdateUser], json_data):
    try:
        model = schema(**json_data)
        validated_data = model.model_dump(exclude_none=True)
    except ValidationError as er:
        raise HttpError(400, er.errors())


@app.errorhandler
def error_handler(err: HttpError):
    http_response = jsonify({'status': 'error', 'description': HttpError.errors()})
    http_response.status_code = 400
    return http_response


def get_user(session: Session, user_id: int):
    user = session.get(User, user_id)
    if user is None:
        raise HttpError(404, 'No such user')
    return user


class UsersView(MethodView):

    def get(self, user_id: int):
        with Session() as session:
            user = get_user(session, user_id)
            return jsonify({
                'id': user.id,
                'name': user.name,
                'creation_time': user.creation_time.isoformat()
            })

    def post(self):
        json_data = validate(CreateUser, request.json)
        json_data['password'] = hash_password(json_data['password'])
        with Session() as session:
            user = User(**json_data)
            session.add(user)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, 'User already exists')
            return jsonify({
                'status': 'success',
                'id': user.id
            })

    def patch(self, user_id: int):
        json_data = validate(UpdateUser, request.json)
        with Session() as session:
            user = get_user(session, user_id)
            for field, value in json_data.items():
                setattr(user, field, value)
            session.add(user)
            session.commit()
            return jsonify({
                'status': 'success',
                'id': user.id
            })

    def delete(self, user_id):
        with Session() as session:
            user = get_user(session, user_id)
            session.delete(user)
            session.commit()
            return jsonify({
                'status': 'success',
                'id': user.id
            })


user_view = UsersView.as_view('users')

app.add_url_rule('/users/<int:user_id>', view_func=user_view, methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/users/', view_func=user_view, methods=['POST'])
# @app.route('/')
# def hello():
#     return 'Hello, World!'


if __name__ == '__main__':
    app.run()
