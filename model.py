from flask import Flask
from marshmallow import Schema, fields, pre_load, validate, ValidationError
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

ma = Marshmallow()
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(
        'User',
        backref=db.backref('notes', lazy='dynamic'),
    )

    def __init__(self, title, description, user_id):
        self.title = title
        self.description = description
        self.user_id = user_id


class UserSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str()
    email = fields.Str()
    
# Custom validator
def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')
        
class NoteSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    user = fields.Nested(UserSchema, validate=must_not_be_blank)
    title = fields.Str()
    description = fields.Str()
