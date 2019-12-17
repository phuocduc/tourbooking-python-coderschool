from flask import Blueprint, render_template,request,flash, redirect,url_for, jsonify
from flask_login import current_user, login_required, login_user,logout_user
from src import db, app
from src.models import Tour, Image, Book_tour, Book_tour_items, Contact, Comment
from itsdangerous import URLSafeSerializer,URLSafeTimedSerializer
import requests
from requests.exceptions import HTTPError
from datetime import datetime


product_blueprint = Blueprint('products', __name__)

@product_blueprint.route('/tours', methods=["GET","POST"])
def tour():
    if request.method == "POST":
        try:
            new_tour = Tour(
            title = request.get_json()['title'],
            image_main = request.get_json()['image_main'],
            prices = request.get_json()['prices'],
            content = request.get_json()['content'],
            description = request.get_json()['description'],
            duration_day = request.get_json()['duration_day'],
            status = request.get_json()['status'])
            db.session.add(new_tour)
            db.session.commit()
            # print("success")dddd
            # return make_response(jsonify({"state": "add_success"}, 200)
            # return jsonify()
            return jsonify({
                "id": new_tour.id, 
                "title": new_tour.title, 
                "image_main": new_tour.image_main, 
                "prices": new_tour.prices, 
                "content": new_tour.content, 
                "description": new_tour.description, 
                "duration_day": new_tour.duration_day,
                "created_at": new_tour.created_at,
                "updated_at": new_tour.updated_at,
                "status": new_tour.status,
                "state" : "success"
                            }), 200
        except expression as identifier:
            return jsonify({}), 500
    tours = Tour.query.order_by(Tour.id.desc()).all()
    return jsonify({"tours":[tour.render() for tour in tours]})
        


@product_blueprint.route('/tours/<id>', methods=['GET', 'POST', "DELETE"])
def tour_child(id):
    tour = Tour.query.filter_by(id = id).first()
    if request.method == "DELETE":
        db.session.delete(tour)
        db.session.commit()
        return jsonify({"state": "delete_success"})
    if request.method == "POST":
        tour.title = request.get_json()['title']
        tour.image_main = request.get_json()['image_main']
        tour.prices = request.get_json()['prices']
        tour.content = request.get_json()['content']
        tour.description = request.get_json()['description']
        tour.status = request.get_json()['status']
        tour.duration_day = request.get_json()['duration_day']
        db.session.commit()
        return jsonify({"state": "success_change"})
    return jsonify({
                        "title": tour.title,
                        "image_main": tour.image_main,
                        "prices" : tour.prices, 
                        "content": tour.content,
                        "description": tour.description,
                        "duration_day": tour.duration_day,
                        "status": tour.status,
                        "created_at": tour.created_at,
                        "updated_at": tour.updated_at,
                        })

@product_blueprint.route('/destinations/<id>', methods=['GET','POST'])
def render_ATour(id):
    tour = Tour.query.filter_by(id=id).first()
    return jsonify({
        "tour" : tour.render()
    })


@product_blueprint.route('/tours/<id>/book-tour', methods=['GET','POST'])
def book_tour(id):
    if request.method == "POST":
        tourBook = Book_tour(tour_id=id, payment=request.get_json()['payment'],
                             first_name=request.get_json()['first_name'],
                             last_name=request.get_json()['last_name'],
                             country=request.get_json()['country'],
                             languages = request.get_json()['languages'],
                             book_date = request.get_json()['book_date'],
                             phone=request.get_json()['phone'],
                             email=request.get_json()['email'])
        db.session.add(tourBook)
        db.session.commit()
    if request.method == "DELETE":
        tour = Book_tour.query.filter_by(id=id).first()
        db.session.delete(tour)
        db.session.commit()
        return jsonify({"state": "delete_success"})

@product_blueprint.route('/book-tour', methods=["GET"])
def render_bookTour():
    books = Book_tour.query.order_by(Book_tour.id.desc()).all()
    return jsonify({
            "book": [book.render() for book in books]
        })

@product_blueprint.route('/contact', methods=["GET","POST"])
def contact():
    if request.method == "POST":
        new_contact = Contact(title=request.get_json()['title'],
                              comment=request.get_json()['comment'],
                              name= request.get_json()['name'],
                              email = request.get_json()['email'])
        db.session.add(new_contact)
        db.session.commit()
        return jsonify({"state": "success"})
    if request.method == "GET":
        contacts = Contact.query.order_by(Contact.id.desc()).all()
        return jsonify({
            "contact" : [contact.render() for contact in contacts]
        })

@product_blueprint.route('/contact/<id>', methods=['DELETE', 'POST'])
def contact_child(id):
    contact = Contact.query.filter_by(id=id).first()
    if request.method == "DELETE":
        db.session.delete(contact)
        db.session.commit()
        return jsonify({"state" : "success"})
    if request.method == "POST":
        contact.title = request.get_json()['title']
        contact.comment = request.get_json()['comment']
        contact.name = request.get_json()['name']
        contact.email = request.get_json()['email']
        db.session.commit()
        return jsonify({"state": "success"})


@product_blueprint.route('/tours/<id>/pictures', methods=['GET','POST'])
def images(id):
    if request.method == "POST":
        try:
            new_image = Image(
                      img_first=request.get_json()['img_first'],
                      content_first=request.get_json()['content_first'],
                      img_second=request.get_json()['img_second'],
                      content_second=request.get_json()['content_second'],
                      img_third=request.get_json()['img_third'],
                      content_third=request.get_json()['content_third'],
                      tour_id = id
                      )
            db.session.add(new_image)
            db.session.commit()
            return jsonify({
                    "img_1" : new_image.img_first,
                    "content_1" : new_image.content_first,
                    "img_2" : new_image.img_second,
                    "content_2" : new_image.content_second,
                    "img_3" : new_image.img_third,
                    "content_3" : new_image.content_third,
                    "tourId" : new_image.tour_id,
                    "state" : "success"
                    }),200
        except expression as identifier:
            return jsonify({}), 500
    if request.method == "GET":
        images = Image.query.filter_by(tour_id=id).all()
        return jsonify({
            "Image" : [image.render() for image in images], "state" : "success"
        })
    

@product_blueprint.route('/pictures/<id>', methods=['POST','DELETE','GET'])
def picture_child(id):
    image = Image.query.filter_by(tour_id=id).first()
    if request.method == "DELETE":
        try:
            db.session.delete(image)
            db.session.commit()
            return jsonify({"state" : "success"}),200
        except expression as identifier:
            return jsonify({}),500
    if request.method == "POST":
        imageUpdate = Image.query.filter_by(id=id).first()
        imageUpdate.img_first = request.get_json()['img_first']
        imageUpdate.content_first = request.get_json()['content_first']
        imageUpdate.img_second = request.get_json()['img_second']
        imageUpdate.content_second = request.get_json()['content_second']
        imageUpdate.img_third = request.get_json()['img_third']
        imageUpdate.content_third = request.get_json()['content_third']
        db.session.commit()
        return jsonify({"state": "success", "tour_id" : imageUpdate.tour_id}),200
    if request.method == "GET":
        image = Image.query.filter_by(id=id).first()
        return jsonify({
        "image" : image.render()
    })

@product_blueprint.route('/book-tour/<id>', methods=['GET','POST'])
def check_booktour(id):
    tour = Tour.query.filter_by(id=id).first()
    if request.method == "POST":
        book_tour = Book_tour(
            languages = request.get_json()['languages'],
            dates = request.get_json()['dates'],
            number_people = request.get_json()['number'],
            image = tour.image_main,
            name_tour = tour.title,
            prices = tour.prices,
            tour_id = id
        )
        db.session.add(book_tour)
        db.session.commit()
        return jsonify({
            "id" : book_tour.id,
            "languages" : book_tour.languages,
            "dates" : book_tour.dates,
            "number_people" : book_tour.number_people,
            "tour_id" : book_tour.tour_id,
            "name" : book_tour.name_tour,
            "image" : book_tour.image,
            "prices" : book_tour.prices,
            "state" : "success"
        })
    book_tour = Book_tour.query.filter_by(id=id).first()
    return jsonify({

        "book_tour" : book_tour.render()
    })

@product_blueprint.route('/checkout/<id>', methods=['GET','POST'])
def checkout(id):
    book_tour = Book_tour.query.filter_by(id=id).first()
    if request.method == "POST":
        book_item = Book_tour_items(
            book_tourItem_id = id,
            payment = book_tour.prices * book_tour.number_people,
            languages = book_tour.languages,
            book_date = book_tour.dates,
            tour_name = book_tour.name_tour,
            first_name = request.get_json()['firstname'],
            last_name = request.get_json()['lastname'],
            country = request.get_json()['country'],
            phone = request.get_json()['phone'],
            email = request.get_json()['email']
            )
        db.session.add(book_item)
        db.session.commit()
        send_confirm(book_item.id)
        return jsonify({
            "book_item_id" : book_item.book_tourItem_id,
            "payment" : book_item.payment,
            "languages" : book_item.languages,
            "book_date" : book_item.book_date,
            "tour_name" : book_item.tour_name,
            "first_name" : book_item.first_name,
            "last_name" : book_item.last_name,
            "country" : book_item.country,
            "phone" : book_item.phone,
            "email" : book_item.email,
            "state" : "success"
        })



def send_confirm(id):
    confirm = Book_tour_items.query.filter_by(id=id).first()
    s = URLSafeTimedSerializer(app.secret_key)
    send_email(confirm.email,confirm.id)
    print(confirm.email)
    print(app.config['API_EMAIL'])
    print("confirm")
    return jsonify({"state" : "success"})


def send_email(email,id):
    confirmInfo = Book_tour_items.query.filter_by(id=id).first()
    # payments = confirmInfo.payment
    # formatPayment = locale.currency(payments,grouping=True)
    time = confirmInfo.book_date
    formatDate = time.strftime("%A,%d %B,%Y")
    url= "https://api.mailgun.net/v3/sandbox172ed4b367ea4418b3ef4ee81fc88b7b.mailgun.org/messages"
    try:

        response = requests.post(url,
            auth=("api", app.config['API_EMAIL']),
            data=
            {"from": "<ducnpgt60935@fpt.edu.vn>",
                "to": [email],
                "subject": "Tour Confirm",
                "text": f"Dear {confirmInfo.first_name},\n\nThis email just let you know that your tour is on ready now! \nPlease check for sure your information \n\nYour Tour: {confirmInfo.tour_name}\nYour First Name: {confirmInfo.first_name}\nYour Last Name: {confirmInfo.last_name}\nThe languages you will use:  {confirmInfo.languages}\nYour Booking Date: {formatDate}\nYour Country: {confirmInfo.country}\nPhone: {confirmInfo.phone}\nEmail: {confirmInfo.email}\nTour Payment:  {confirmInfo.payment} vnd\n\nThank for your information and we will contact you soon..\nHave a nice day!"})
                
        # If the response was successful, no Exception will be raised
        response.raise_for_status()

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')



@product_blueprint.route('/comment/<id>',methods=['GET','POST','DELETE'])
def comment(id):
    if request.method == "POST":
        new_comment = Comment(
             user = request.get_json()['user'], tour_id = id,
            comment= request.get_json()['comment_tour']

        )
        db.session.add(new_comment)
        db.session.commit()
        return jsonify({
            "id": new_comment.id,
            "user": new_comment.user,
            "tour_id": new_comment.tour_id,
            "comment": new_comment.comment
            })
    if request.method == "GET":
        comments = Comment.query.filter_by(tour_id = id).order_by(Comment.id.desc()).all()
        return jsonify({
        "comment" :[comment.render() for comment in comments] 
        })
    if request.method == "DELETE":
        remove_comment = Comment.query.filter_by(id=id).first()
        if remove_comment.user == request.get_json()['user']:
            db.session.delete(remove_comment)
            db.session.commit()
            return jsonify({"state": "success"})
        return jsonify({'state' : 'notUser'})