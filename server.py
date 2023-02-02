from app import get_app
from views import UserOps, AdvertisementOps
from errors import HttpException, error_handler

app = get_app()

app.add_url_rule('/users/<int:user_id>/', view_func=UserOps.as_view('users'),
                 methods=['GET', 'DELETE', 'PATCH'])
app.add_url_rule('/users/', view_func=UserOps.as_view('user_create'),
                 methods=['POST'])
app.add_url_rule('/adv/<int:adv_id>/', view_func=AdvertisementOps.as_view('advertisements'),
                 methods=['GET', 'DELETE', 'PATCH'])
app.add_url_rule('/adv/<int:user_id>/', view_func=AdvertisementOps.as_view('advertisements_create'),
                 methods=['POST'])
app.errorhandler(HttpException)(error_handler)

if __name__ == '__main__':
    app.run()
