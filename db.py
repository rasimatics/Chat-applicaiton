from pymongo import MongoClient
from werkzeug.security import generate_password_hash


client = MongoClient('mongodb+srv://helloworld:helloworld@cluster0.ebecx.mongodb.net/ChatApp?retryWrites=true&w=majority')

chat_db = client.get_database('ChatApp')
user_collection = chat_db.get_collection('users')

def save_user(username,email,password):
    password = generate_password_hash(password)
    user_collection.insert_one({'_id':username,"email":email,"password":password})


