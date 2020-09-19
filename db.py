from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from user import User
from datetime import datetime
from bson.objectid import ObjectId
import bson
import random

# mongoDb connection
client = MongoClient('mongodb+srv://helloworld:helloworld@cluster0.ebecx.mongodb.net/ChatApp?retryWrites=true&w=majority')

# get database
chat_db = client.get_database('ChatApp')
# get table
user_collection = chat_db.get_collection('users')
room_collection = chat_db.get_collection('rooms')
member_collection = chat_db.get_collection('members')
messages_collection = chat_db.get_collection('messages')

def save_user(username,email,password):
    password = generate_password_hash(password)
    # insert data
    user_collection.insert_one({'_id':username,"email":email,"password":password})

def get_user(username):
    # get data
    user = user_collection.find_one({'_id':username})
    return User(user['_id'],user['email'],user['password']) if user is not None else None

def create_room(username,room_name,num_member):
    room_id = room_collection.insert_one({'_id':room_name,'created_by':username,'n_members':bson.Int64(num_member),'created_at':datetime.now()})
    add_member(username,room_name)

def add_member(username,room_name):
    room = room_collection.find_one({'_id':room_name})
    member_collection.insert_one({'room_name': room_name,'username':username,'added_at': datetime.now()})
    room_collection.find_one_and_update({'_id':room_name},{'$inc':{'n_members':-1}})


def get_num_of_members(room_name):
    room = room_collection.find_one({'_id':room_name})
    return room['n_members']    

def check_is_member(username,room_name):
   return member_collection.find_one({'room_name':room_name,'username':username})


def save_message(message,username,room_name):
    messages_collection.insert_one({'message':message,'username':username,'room_name':room_name,'created_at': datetime.now()})

def get_messages(room_name):
    return list(messages_collection.find({"room_name":room_name},{"_id":0}))

