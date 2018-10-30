from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from model import User, UserSchema, Note, NoteSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

#schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)

note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)

#routes
@app.route("/")
def index():
    
    return jsonify({'message': 'hello world'}), 200


@app.route("/users", methods=["GET"])
def get_user():
    users = User.query.all()
    result = users_schema.dump(users)
    
    return jsonify({'users': result})


@app.route("/user", methods=["POST"])
def add_user():
    username = request.json['username']
    email = request.json['email']
    
    new_user = User(username, email)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)


@app.route('/user/<int:pk>')
def get_users(pk):
    try:
        user = User.query.get(pk)
    except IntegrityError:
        return jsonify({'message': 'User could not be found.'}), 400
        
    user_result = user_schema.dump(user)
    notes_result = notes_schema.dump(user.notes.all())
    return jsonify({'user': user_result, 'notes': notes_result})


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

    return note_schema.jsonify(new_note)


@app.route("/notes", methods=["GET"])
def get_notes():
    notes = Note.query.all()
    result = notes_schema.dump(notes, many=True)
    
    return jsonify({'notes': result})
    

@app.route('/note/<int:pk>')
def get_note(pk):
    try:
        note = Note.query.get(pk)
    except IntegrityError:
        return jsonify({'message': 'Quote could not be found.'}), 400
    result = note_schema.dump(note)
    return jsonify({'note': result})


#__init__
if __name__ == '__main__':
    app.run(debug=True)