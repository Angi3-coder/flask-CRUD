from flask import Flask, jsonify, request
from flask_migrate import Migrate
#import models
from models import User, db

#create app
app = Flask(__name__)

# Configure the database (SQLite for simplicity)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
#dont keep track of the changes
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)
migrate = Migrate(app, db)
# Import models here to register them with SQLAlchemy
# from models import User

@app.route('/')
def home():
    return "<h1>Hello</h1>"
#CRUD OPERATIONS
#READ method= GET
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    #create an empty list to store user
    output = []

    #go through each user and add info to the empty list
    for user in users:
        user_data = {
            'id': user.id,
            'name':user.username,
            'email':user.email
        }
        output.append(user_data)

    #return the list an JSON
    return jsonify(output)


#get user by their id
@app.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    #get user by their id
    user = User.query.get(id)

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    #create dictionary with the user info
    user_data = {
        'id': user.id,
        'name':user.username,
        'email':user.email
    }

    return jsonify(user_data)


#Create user method=POST
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(username= data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message':"User Created successfully"}), 201


#Update methods=PUT
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    data = request.get_json()
    user.username = data.get('name', user.username)
    user.email = data.get('email', user.email)

    #commit changes
    db.session.commit()

    return jsonify({'message': 'User Updated Successfully'})

if __name__ == '__main__':
    app.run(debug=True)