from typing import Type
from flask import Flask, jsonify, request
from flask.views import MethodView
from pydantic import ValidationError
from
from models import Session, User
from schema import CreateUser, UpdateUser

app = Flask(__name__)


class HttpError(Exception):
    def __init__(self, status_code: int, error_message: dict | list | str):
        self.status_code = status_code
        self.error_message = error_message


def validate(schema: Type[CreateUser] | Type[UpdateUser], json_data):
    try:
        model = schema(**json_data)
        validated_data = model.dict(exclude_none=True)
    except ValidationError as er:
        raise HttpError(400, er.errors())


@app.errorhandler
def error_handler(err: HttpError):
    http_response = jsonify({'status': 'error', 'description': HttpError.errors()})
    http_response.status_code = 400
    return http_response


class UsersView(MethodView):

    def get(self):
        pass

    def post(self):
        json_data = validate(CreateUser, request.json)

        with Session() as session:
            user = User(**json_data)
            session.add(user)
            session.commit()
            return jsonify({
                'status': 'success',
                'id': user.id
            })


    def patch(self):
        pass

    def delete(self):
        pass


user_view = UsersView.as_view('users')

app.add_url_rule('/users/<int:user_id>', view_func=user_view, methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/users/', view_func=user_view, methods=['POST'])
# @app.route('/')
# def hello():
#     return 'Hello, World!'


if __name__ == '__main__':
    app.run()
