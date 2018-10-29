from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from model import User, UserSchema, Note, NoteSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)
ma = Marshmallow(app)

#schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)

note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)

#routes
@app.route("/")
def index():
    return "Hello"


@app.route("/user", methods=["POST"])
def add_user():
    username = request.json['username']
    email = request.json['email']
    
    new_user = User(username, email)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)


@app.route("/users", methods=["GET"])
def get_user():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)


@app.route("/user/<id>", methods=["GET"])
def user_detail(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)


@app.route("/user/<id>", methods=["PUT"])
def user_update(id):
    user = User.query.get(id)
    username = request.json['username']
    email = request.json['email']

    user.email = email
    user.username = username

    db.session.commit()
    return user_schema.jsonify(user)


@app.route("/user/<id>", methods=["DELETE"])
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)
    
    
@app.route("/note", methods=["POST"])
def add_note():
    title = request.json['title']
    description = request.json['description']
    user_id = request.json['user_id']
    
    new_note = Note(title, description, user_id)

    db.session.add(new_note)
    db.session.commit()

    return user_schema.jsonify(new_note)


@app.route("/notes", methods=["GET"])
def get_notes():
    all_notes = Note.query.all()
    result = notes_schema.dump(all_notes)
    return jsonify(result.data)
    
    
@app.route("/note/<id>", methods=["DELETE"])
def note_delete(id):
    note = Note.query.get(id)
    db.session.delete(note)
    db.session.commit()

    return user_schema.jsonify(note)


#__init__
if __name__ == '__main__':
    app.run(debug=True)