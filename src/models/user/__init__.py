from flask_login import UserMixin, current_user
from src import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin



class User(UserMixin,db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(120))
    role = db.Column(db.Boolean, default = False)

    def set_password(self,password):
        self.password = generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password,password)
    def check_user(self):
        return User.query.filter_by(email=self.email).first()

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in  self.__table__.columns}
    
class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User)

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User)

