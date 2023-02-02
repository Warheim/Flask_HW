from flask import Flask, request, jsonify
from flask.views import MethodView
from database import Session, UserModel, AdvertisementModel
from errors import HttpException
from hashlib import md5
from sqlalchemy.exc import IntegrityError
from validators import CreateUserValidator, PatchUserValidator, CreateAdvValidator, PatchAdvValidator, validate

app = Flask('app')


@app.errorhandler(HttpException)
def error_handler(error: HttpException):
    response = jsonify({
        'status': 'error',
        'status_code': error.status_code,
        'message': error.message
    })
    return response


def get_user(user_id: int, session=Session) -> UserModel:
    user = session.query(UserModel).get(user_id)
    if user is None:
        raise HttpException(
            status_code=404,
            message='user not found'
        )
    return user


def get_adv(adv_id: int, session=Session) -> AdvertisementModel:
    adv = session.query(AdvertisementModel).get(adv_id)
    if adv is None:
        raise HttpException(
            status_code=404,
            message='advertisement not found'
        )
    return adv


class UserOps(MethodView):

    def get(self, user_id: int):
        with Session() as session:
            user = get_user(user_id, session)
            return jsonify({
                'id': user.id,
                'email': user.email
            })

    def post(self):
        user_data = validate(request.json, CreateUserValidator)
        user_data['password'] = md5((user_data.get('password')).encode('utf-8')).hexdigest()
        with Session() as session:
            new_user = UserModel(**user_data)
            session.add(new_user)
            try:
                session.commit()
            except IntegrityError:
                raise HttpException(
                    status_code=409,
                    message='user with this email already exists'
                )
            return jsonify({'status': f'new user is {new_user.email}'})

    def patch(self, user_id: int):
        user_data = validate(request.json, PatchUserValidator)
        if user_data.get('password'):
            user_data['password'] = md5((user_data.get('password')).encode('utf-8')).hexdigest()
        with Session() as session:
            change_user = get_user(user_id, session)
            for field, value in user_data.items():
                setattr(change_user, field, value)
            session.add(change_user)
            session.commit()
        return jsonify({'status': 'user data changed'})

    def delete(self, user_id: int):
        with Session() as session:
            old_user = get_user(user_id, session)
            session.delete(old_user)
            session.commit()
        return jsonify({'status': f'user {old_user.email} deleted'})


class AdvertisementOps(MethodView):

    def get(self, adv_id: int):
        with Session() as session:
            adv = get_adv(adv_id, session)
            return jsonify({
                'id': adv.id,
                'title': adv.title,
                'description': adv.description,
                'author': adv.author,
                'creation_date': adv.creation_date
            })

    def post(self, user_id: int):
        adv_data = validate(request.json, CreateAdvValidator)
        with Session() as session:
            user = get_user(user_id, session)
            adv_data['author'] = user.id
            new_adv = AdvertisementModel(**adv_data)
            session.add(new_adv)
            session.commit()
        return jsonify({'status': 'advertisement added'})

    def patch(self, adv_id: int):
        adv_data = validate(request.json, PatchAdvValidator)
        with Session() as session:
            adv = get_adv(adv_id, session)
            for field, value in adv_data.items():
                setattr(adv, field, value)
            session.add(adv)
            session.commit()
        return jsonify({'status': 'advertisement changed'})

    def delete(self, adv_id: int):
        with Session() as session:
            old_adv = get_adv(adv_id, session)
            session.delete(old_adv)
            session.commit()
        return jsonify({'status': 'advertisement deleted'})


app.add_url_rule('/users/<int:user_id>/', view_func=UserOps.as_view('users'),
                 methods=['GET', 'DELETE', 'PATCH'])
app.add_url_rule('/users/', view_func=UserOps.as_view('user_create'),
                 methods=['POST'])
app.add_url_rule('/adv/<int:adv_id>/', view_func=AdvertisementOps.as_view('advertisements'),
                 methods=['GET', 'DELETE', 'PATCH'])
app.add_url_rule('/adv/<int:user_id>/', view_func=AdvertisementOps.as_view('advertisements_create'),
                 methods=['POST'])

if __name__ == '__main__':
    app.run()
