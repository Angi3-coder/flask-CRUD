from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate
from models import User, db
from flask_restful import Api, Resource

#create an app
app = Flask(__name__)

#config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

#initialize an API
api = Api(app)

class UserResource(Resource):
    #get users
    def get(self):
        users = User.query.all()
        output =[]
        for user in users:
            user_dict= {
                "id": user.id,
                "name": user.username,
                "email":user.email
            }
            output.append(user_dict)
        return make_response(jsonify(output), 200)
    
    #post user
    def post(self):
        data = request.get_json()
        new_user= User(username = data['name'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()

        return make_response(jsonify({"message": "User created succesfully"}), 201)
    

api.add_resource (UserResource, '/users')


if __name__ == '__main__':
    app.run(debug=True)