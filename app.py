from os import urandom
from flask import Flask, request, jsonify, request, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from model import User, UserSchema, Note, NoteSchema
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

#schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)

note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)

@login_manager.user_loader
def load_user(user_email):
    return User.query.filter_by(email = user_email).first()

#routes
@app.route("/login", methods=["POST"])
def login():
    """For GET requests, display the login form.
    For POSTS, login the current user by processing the form.
    """
    user = User.query.filter_by(username = request.json['username']).first()
    password = request.json['password']
    
    if user != None and password != None:
        if bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return jsonify({'message': 'User authenticated'}), 200
        else:
            return jsonify({'message': 'Password incorrect'}), 400
    else:
        return jsonify({'message': 'Username incorrect'}), 400
    

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    
    return jsonify({'message': 'user logout'}), 200
    

@login_manager.unauthorized_handler
def unauthorized_handler():
    
    return jsonify({'message': 'Unauthorized, please login!'}), 400
    
    
@app.route("/")
@login_required
def index():
    
    return jsonify({'message': 'hello world'}), 200



@app.route("/users", methods=["GET"])
@login_required
def get_user():
    users = User.query.all()
    result = users_schema.dump(users)
    
    return jsonify({'users': result})
    

@app.route("/user", methods=["POST"])
def add_user():
    username = request.json['username']
    email = request.json['email']
    password = bcrypt.generate_password_hash(request.json['password'])
    
    new_user = User(username, email, password)

    db.session.add(new_user)
    db.session.commit()
    
    return user_schema.jsonify(new_user)


@app.route('/user/<int:pk>')
@login_required
def get_users(pk):
    try:
        user = User.query.get(pk)
    except IntegrityError:
        return jsonify({'message': 'User could not be found.'}), 400
        
    user_result = user_schema.dump(user)
    notes_result = notes_schema.dump(user.notes.all())
    
    return jsonify({'user': user_result, 'notes': notes_result})


@app.route("/user/<id>", methods=["PUT"])
@login_required
def user_update(id):
    user = User.query.get(id)
    username = request.json['username']
    email = request.json['email']

    user.email = email
    user.username = username

    db.session.commit()
    
    return user_schema.jsonify(user)


@app.route("/user/<id>", methods=["DELETE"])
@login_required
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)
    
    
@app.route("/note", methods=["POST"])
@login_required
def add_note():
    title = request.json['title']
    description = request.json['description']
    user_id = request.json['user_id']
    
    new_note = Note(title, description, user_id)

    db.session.add(new_note)
    db.session.commit()

    return note_schema.jsonify(new_note)


@app.route("/notes", methods=["GET"])
@login_required
def get_notes():
    notes = Note.query.all()
    result = notes_schema.dump(notes, many=True)
    
    return jsonify({'notes': result})
    

@app.route('/note/<int:pk>')
@login_required
def get_note(pk):
    try:
        note = Note.query.get(pk)
    except IntegrityError:
        return jsonify({'message': 'Quote could not be found.'}), 400
    result = note_schema.dump(note)
    
    return jsonify({'note': result})


#__init__
if __name__ == '__main__':
    app.secret_key = urandom(24)
    # Pick one of redis, memcached, filesystem or mongodb.
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)