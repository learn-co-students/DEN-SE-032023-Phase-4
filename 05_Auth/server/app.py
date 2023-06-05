# export FLASK_APP=app.py
# export FLASK_RUN_PORT=5555
# flask db init
# flask db revision --autogenerate -m 'Create tables' 
# flask db upgrade 

# Standard imports/boilerplate setup (We added session)
from flask import Flask, request, make_response, jsonify, session
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS
from models import db, User
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)
CORS(app)
bcrypt = Bcrypt(app)
#1. ✅ python -c 'import os; print(os.urandom(16))'
#Used to hash the session data
app.secret_key = b'\xb8C\xack"}]c_\xb7\xf0\xcdng\xe7\xdf'

# 2.✅ Create a Login route
    # 3.1 Create a login class that inherits from Resource
    # 3.2 Use api.add_resource to add the '/login' path
    # 3.3 Build out the post method
        # 3.3.1 convert the request from json and select the user name sent form the client. 
        # 3.3.2 Use the name to query the user with a .filter
        # 3.3.3 If found set the user_id to the session hash
        # 3.3.4 convert the user to_dict and send a response back to the client 
class Users(Resource):
     def post(self):
        form_json = request.get_json()
        new_user = User(
            name=form_json['name'],
        )
        new_user.password = form_json['password']
        db.session.add(new_user)
        print(new_user)
        db.session.commit()
        session['user_id'] = new_user.id
        return make_response(
            new_user.to_dict(),
            201,
        )
api.add_resource(Users, '/login')

class login(Resource):
    def post(self):
        data = request.get_json()
        name = data['name']
        password = data['password']
        user = User.query.filter_by(name=name).first()
        if user and user.authenticate(password):
            session['user_id'] = user.id  # Set the user_id in the session
            return make_response(user.to_dict(), 200)
        else:
            return make_response("Invalid credentials", 401)
api.add_resource(login, '/signin')

# 3.✅ Create a check login route that will save the user to the session
class check_login(Resource):
    def post(self):
        data = request.get_json()
        name = data['name']
        password = data['password']
        user = User.query.filter_by(name=name).first()
        if user and user.authenticate(password):
            session['user_id'] = user.id  # Set the user_id in the session
            return make_response(user.to_dict(), 200)
        else:
            return make_response("Invalid credentials", 401)
api.add_resource(check_login, '/check_login')

# 4. Create a logout route now! set session to None
class logout(Resource):
    def delete(self):
        session['user_id'] = None
        return make_response(
            "Logged out",
            200,
        )
api.add_resource(logout, '/logout')
# Use @app.before_request, to run a function before every request

@app.before_request
def check_session():
    print(session)
    if session.get("user_id") is None:
        session["user_id"] = None
    else:
        print("User is logged in")
        print(session["user_id"])


if __name__ == '__main__':
    app.run(port=5555)