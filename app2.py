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

#Resource to get by id
class SingleUserResource(Resource):
    #get user by id
    def get(self, id):
        user = User.query.get(id)

        if not user:
            return make_response(jsonify({"error": "User not Found"}), 404)
        
        user_data = {
            "id": user.id,
            "name": user.username,
            "email": user.email
        }

        return make_response(jsonify(user_data))
    

    #Update
    def put(self, id):
        user = User.query.get(id)

        #if user is not found
        if not user:
            return make_response(jsonify({"Error": "User not found"}), 404)
        
        data = request.get_json()

        if not 'name' in data:
            return make_response(jsonify({"Error": "Name cannot be empty"}))
        
        user.username = data['name']
        user.email= data['email']

        db.session.commit()

        return make_response(jsonify({"Message": "User Updated Successfully"}), 200)
    

    def delete(self, id):
        user = User.query.get(id)

        if not user:
            return make_response(jsonify({"Error":"User not found"}), 404)
        
        db.session.delete(user)
        db.session.commit()

        return make_response(jsonify({"Message":"User deleted Successfully"}), 200)

api.add_resource(SingleUserResource, '/users/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)