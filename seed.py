#Seeding script - for pre-filling the database with test data
#               -creates user examples and commits them to the database
#               -imports app and models

from app import app
from models import User, db

#use app contxt
with app.app_context():
    #optional: Clear the database
    User.query.delete()

    #Add users
    user1 = User(username= "Alice", email="alice@gmail.com")
    user2 = User(username= "Jane", email="jane@gmail.com")
    user3 = User(username= "John", email="john@gmail.com")
    user4 = User(username= "Bob", email="bob@gmail.com")
    user5 = User(username= "Charlie", email="charlie@gmail.com")

    #add users to session
    db.session.add_all([user1,user2,user3,user4,user5])
    #commit users  from session to database
    db.session.commit()

    print("Seeding is successful")
