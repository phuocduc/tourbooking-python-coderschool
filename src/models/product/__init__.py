from flask import Flask
from src import db



class Tour(db.Model):
    __tablename__="tours"
    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.Text, nullable=True)
    image_main = db.Column(db.Text)
    prices = db.Column(db.Integer, nullable=True)
    content = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now() , nullable=True)
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now(),nullable=True)
    status = db.Column(db.String(255), nullable=True)
    duration_day = db.Column(db.Integer, nullable=False)
    book_tour = db.relationship('Book_tour', backref="tourId", lazy=True)
    img_tour = db.relationship('Image', backref="tourId_img", uselist=False )

    order_tour = db.relationship('Book_tour', backref="tourId_bookTour", lazy=True)
    tour_comments = db.relationship('Comment', backref="tour_comment_id", lazy=True)

    def render(self):
        return {
            "id":self.id,
            "image_main":self.image_main,
            "title":self.title,
            "prices":self.prices,
            "content":self.content,
            "duration_day":self.duration_day,
            "description":self.description,
            "created_at":self.created_at,
            "updated_at":self.updated_at,
            "status":self.status,
        }



class Image(db.Model):
    __tablename__="images"
    id = db.Column(db.Integer, primary_key=True)
    img_first = db.Column(db.Text, nullable = True)
    content_first = db.Column(db.Text, nullable = True)
    img_second = db.Column(db.Text, nullable = True)
    content_second = db.Column(db.Text, nullable = True)
    img_third = db.Column(db.Text, nullable = True)
    content_third = db.Column(db.Text, nullable = True)
    tour_id = db.Column(db.Integer, db.ForeignKey('tours.id'), nullable=True)    
    def render(self):
        return {
            "id": self.id,
            "img_first": self.img_first,
            "content_first": self.content_first,
            "img_second": self.img_second,
            "content_second": self.content_second,
            "img_third": self.img_third,
            "content_third": self.content_third,
            "tour_id": self.tour_id,
        }

class Book_tour(db.Model):
    __tablename__ = "book_tours"
    id = db.Column(db.Integer, primary_key=True)
    languages = db.Column(db.String(255), nullable=True)
    dates = db.Column(db.Date, nullable=True)
    number_people = db.Column(db.Integer, nullable=True)
    image = db.Column(db.Text,nullable=True)
    name_tour = db.Column(db.String(255),nullable=True)
    prices = db.Column(db.Integer,nullable=True)
    tour_id = db.Column(db.Integer, db.ForeignKey('tours.id'), nullable = False)
    booktour_items = db.relationship('Book_tour_items', backref="booktour_id", uselist= False)
    def render(self):
        return {
            "id" : self.id,
            "languages" : self.languages,
            "dates" : self.dates,
            "image" : self.image,
            "name_tour" : self.name_tour,
            "prices" : self.prices,
            "number_people" : self.number_people,
            "tour_id" : self.tour_id,
        }
class Book_tour_items(db.Model):
    __tablename__ = 'book_tour_items'
    id = db.Column(db.Integer, primary_key=True)
    book_tourItem_id = db.Column(db.Integer, db.ForeignKey('book_tours.id'), nullable = False)
    payment = db.Column(db.Integer, nullable=False)
    languages = db.Column(db.String(255), nullable=True)
    tour_name = db.Column(db.String(255),nullable=True)
    book_date = db.Column(db.Date, nullable=True)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    country = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable = False)
    # ExpInfo = db.relationship('Exp', backref="product_exp", useList=False)  #one to one
    def render(self):
        return {
            "id" : self.id,
            "tour_id": self.tour_id,
            "payment": self.payment,
            "languages": self.languages,
            "tour_name": self.tour_name,
            "book_date": self.book_date,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "country" : self.country,
            "phone": self.phone,
            "email" : self.email
        }



class Contact(db.Model):
    __tablename__="contacts"
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.Text, nullable=True)
    comment = db.Column(db.Text, nullable=True)
    name = db.Column(db.Text, nullable=True)
    email = db.Column(db.Text, nullable=True)

    def render(self):
        return {
            "id": self.id,
            "title" : self.title,
            "comment": self.comment,
            "name" : self.name,
            "email" : self.email
        }

class Comment(db.Model):
    __tablename__="comments"
    id = db.Column(db.Integer,primary_key = True)
    user = db.Column(db.String(255),nullable=True)
    tour_id = db.Column(db.Integer, db.ForeignKey('tours.id'), nullable=False)
    comment = db.Column(db.Text,nullable=True)

    def render(self):
        return{
            "id": self.id,
            "user": self.user,
            "tour_id": self.tour_id,
            "comment": self.comment
        }

