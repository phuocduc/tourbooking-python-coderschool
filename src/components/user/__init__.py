from flask import Blueprint, render_template,request,flash, redirect,url_for, jsonify
from flask_login import current_user, login_required, login_user,logout_user
from src import db, app
from src.models import User, Token, OAuth
from itsdangerous import URLSafeSerializer,URLSafeTimedSerializer
import requests
from requests.exceptions import HTTPError
import uuid

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/register/', methods=['POST', 'OPTIONS'])
def register():
    if current_user.is_authenticated:
        print("not need to login")
    if request.method == "POST":
        check_user = User.query.filter_by(email = request.get_json()['email']).first()
        if not check_user:
            new_user = User(username = request.get_json()['username'], email = request.get_json()['email'])
            new_user.set_password(request.get_json()['password'])
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"state": "success"})
        return jsonify({"state" : "user_exist"})
    return jsonify({"state": "fail"})

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    check_user = User.query.filter_by(email=request.get_json()['email']).first()
    if request.method == "POST":
        if check_user:
            if check_user.check_password(request.get_json()['password']):
                token = Token.query.filter_by(user_id = check_user.id).first()
                if not token:
                    token = Token(user_id= check_user.id, uuid=str(uuid.uuid4().hex))
                    db.session.add(token)
                    db.session.commit()
                login_user(check_user)
                return jsonify({"user": check_user.username, 
                                "token" : token.uuid , 
                                "state" : "success", 
                                "name" : check_user.username, 
                                "role" : check_user.role})
            return jsonify({"state": "WrongPass"})
        return jsonify({"state" : "no_user"})

@user_blueprint.route('/getuser', methods=['GET'])
@login_required
def get_user():
    user = User.query.filter_by(username = current_user.username).first()
    try:
        return jsonify({
        "succes":True,
        "name":user.username,
        "role":user.role,
        "email": user.email
    }),200
    except expression as identifier:
        return jsonify({}),500

@app.route("/logout")
@login_required
def logout():
    token = Token.query.filter_by(user_id = current_user.id).first()
    if token:
        db.session.delete(token)
        db.session.commit()
    logout_user()
    print("You have logged out")
    return jsonify({

        'state' : 'logout',
        'success': True
    })

# ffff
#  check user
#  if not user return falihs
# user : check password if fail return 
# if true password:  check token from table token, 
# if not token, create new token for that user, 
# user_login 
# return {} 
# 2 key : user, token
# front end read response: if res === ok: setstate user, save localstorate


    # jsonized_excerpt_objects_list = []
    # for user in users:
    #     jsonized_excerpt_objects_list.append(user.as_dict())

    # return jsonify(jsonized_excerpt_objects_list)


@user_blueprint.route('/forget', methods=['GET','POST'])
def forget():
    if request.method == "POST":
        user = User(email = request.get_json()['email']).check_user()
        if not user:
            print("not user")
        s = URLSafeTimedSerializer(app.secret_key)
        token = s.dumps(user.email, salt="RESET_PASSWORD")
        send_email(token,user.email)
        print(user.email)
        print(app.config['API_EMAIL'])
        print('token', token)
        print("OK")
        return jsonify({"token" : token,
                        "state" : "sucess"})
    return jsonify({"state" : "fail"})


def send_email(token,email):
   
    url= "https://api.mailgun.net/v3/sandbox172ed4b367ea4418b3ef4ee81fc88b7b.mailgun.org/messages"
    try:
        response = requests.post(url,
            auth=("api", app.config['API_EMAIL']),
            data=
            {"from": "<ducnpgt60935@fpt.edu.vn>",
                "to": [email],
                "subject": "Reset Password",
                "text": f"Go to https://vietnamtour.netlify.com/new_password/{token}"})

        # If the response was successful, no Exception will be raised
        response.raise_for_status()

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')


@user_blueprint.route('/new_password', methods=['GET','POST'])
def reset_password():
    data = request.get_json()
    s = URLSafeTimedSerializer(app.secret_key)
    email = s.loads(data['token'], salt="RESET_PASSWORD", max_age=300)
    print(data['token'])
    user= User(email=email).check_user()
    if not user:
        print("invalid token")
        return jsonify({"state": "invalidToken"})
    if request.method == "POST":
        if data['password'] != data['confirm']:
            return jsonify({"state": "notmatch"})
        user.set_password(data['password'])
        db.session.commit()
        return jsonify({"state" : "success"})