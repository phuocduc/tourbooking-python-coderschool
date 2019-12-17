from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object('config.Config')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
db = SQLAlchemy(app)
db.init_app(app)
from src.components.cli import create_db
from src.models import User, Token, OAuth
from src.components.oauth import blueprint
app.register_blueprint(blueprint, url_prefix="/login")
app.cli.add_command(create_db)

migrate = Migrate(app,db)
CORS(app)

login_manager = LoginManager(app)
login_manager.login_view="users.login"


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)



@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Token ', '', 1)
        token = Token.query.filter_by(uuid=api_key).first()
        if token:
            return token.user
    return None

from src.components.user import user_blueprint
app.register_blueprint(user_blueprint, url_prefix="/")


from src.components.product import product_blueprint
app.register_blueprint(product_blueprint, url_prefix="/")


