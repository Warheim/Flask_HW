from flask import Flask, request, jsonify
from flask.views import MethodView
from database import Session, UserModel

app = Flask('app')


class UserOps(MethodView):

    def get(self, user_id: int):
        with Session() as session:
            user = session.query(UserModel).get(user_id)
        return jsonify({'id': user.id,
                        'email': user.email,
                        'password': user.password})

    def post(self):
        user_data = request.json
        with Session() as session:
            new_user = UserModel(**user_data)
            session.add(new_user)
            session.commit()
        return jsonify({'status': 'OK'})

    def delete(self, user_id: int):
        pass


class AdvertisementOps(MethodView):

    def get(self, adv_id: int):
        pass

    def post(self):
        pass

    def delete(self, adv_id: int):
        pass


app.add_url_rule('/users/<int:user_id>/', view_func=UserOps.as_view('users'), methods=['GET', 'DELETE'])
app.add_url_rule('/users/', view_func=UserOps.as_view('user_create'), methods=['POST'])
app.add_url_rule('/adv/<int:adv_id>/', view_func=AdvertisementOps.as_view('advertisements'), methods=['GET', 'DELETE'])
app.add_url_rule('/adv/', view_func=AdvertisementOps.as_view('advertisements_create'), methods=['POST'])

if __name__ == '__main__':
    app.run()
