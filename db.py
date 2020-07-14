from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from user import User

# mongoDb connection
client = MongoClient('mongodb+srv://helloworld:helloworld@cluster0.ebecx.mongodb.net/ChatApp?retryWrites=true&w=majority')

# get database
chat_db = client.get_database('ChatApp')
# get table
user_collection = chat_db.get_collection('users')

def save_user(username,email,password):
    password = generate_password_hash(password)
    # insert data
    user_collection.insert_one({'_id':username,"email":email,"password":password})

def get_user(username):
    # get data
    user = user_collection.find_one({'_id':username})
    return User(user['_id'],user['email'],user['password']) if user is not None else None

