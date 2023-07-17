from flask import Flask, jsonify, request
from flask.views import MethodView

app = Flask(__name__)


class UsersView(MethodView):

    def get(self):
        pass

    def post(self):
        pass

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
