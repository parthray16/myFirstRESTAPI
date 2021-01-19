from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response
from flask_cors import CORS
import random
import string

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
	return 'Hello, world!'

users = { 
   'users_list' :
   [
      { 
         'id' : 'xyz789',
         'name' : 'Charlie',
         'job': 'Janitor',
      },
      {
         'id' : 'abc123', 
         'name': 'Mac',
         'job': 'Bouncer',
      },
      {
         'id' : 'ppp222', 
         'name': 'Mac',
         'job': 'Professor',
      }, 
      {
         'id' : 'yat999', 
         'name': 'Dee',
         'job': 'Aspring actress',
      },
      {
         'id' : 'zap555', 
         'name': 'Dennis',
         'job': 'Bartender',
      }
   ]
}

@app.route('/users/<id>', methods=['GET', 'DELETE'])
def get_user(id):
   if request.method == 'GET':
      if id :
         for user in users['users_list']:
            if user['id'] == id:
               return user
         return ({})
   if request.method == 'DELETE':
      if id:
         for user in users['users_list']:
            if user['id'] == id:
               users['users_list'].remove(user)
               break
         resp = make_response(jsonify(success=True), 204)
         return resp
   return users

@app.route('/users', methods=['GET', 'POST', 'DELETE'])
def get_users():
   if request.method == 'GET':
      search_username = request.args.get('name')
      search_job = request.args.get('job')
      if (search_username != None) and (search_job != None):
         subdict = {'users_list' : []}
         for user in users['users_list']:
            if user['name'] == search_username and user['job'] == search_job:
               subdict['users_list'].append(user)
         return subdict
      elif search_username :
         subdict = {'users_list' : []}
         for user in users['users_list']:
            if user['name'] == search_username:
               subdict['users_list'].append(user)
         return subdict
      return users
   elif request.method == 'POST':
      userToAdd = request.get_json()
      userToAdd['id'] = id_generator()
      users['users_list'].append(userToAdd)
      resp = make_response(jsonify(success=True), 201)
      resp.data = userToAdd
      return resp
   elif request.method == 'DELETE':
      userToDelete = request.get_json()
      users['users_list'].remove(userToDelete)
      resp = make_response(jsonify(success=True), 204)
      return resp
   else:
      return users

def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
   return ''.join(random.choice(chars) for _ in range(size))