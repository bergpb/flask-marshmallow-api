from flask import Flask
from marshmallow import fields
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
ma = Marshmallow(app)

#models - sqlalchemy
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #define a relation with notes
    user = db.relationship('User', backref='notes')
    
    def __init__(self, title, description, user_id):
        self.title = title
        self.description = description
        self.user_id = user_id


#schemas - marshmallowclass
class NoteSchema(ma.ModelSchema):
    class Meta:
        model = Note
        #define fields to show in return
        fields = ('id', 'title', 'description')
        

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        fields = ('username', 'notes')
    #define a relation with notes, one user have many notes
    notes = fields.Nested(NoteSchema, many=True)
        





        
