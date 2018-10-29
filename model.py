from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

ma = Marshmallow()
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='notes')

    def __init__(self, title, description, user_id):
        self.title = title
        self.description = description
        self.user_id = user_id


class UserSchema(ma.Schema):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        
class NoteSchema(ma.Schema):
    class Meta:
        model = Note
        fields = ('id', 'title', 'description', 'user_id')