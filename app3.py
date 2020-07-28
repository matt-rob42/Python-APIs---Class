# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 22:11:46 2020

@author: matt_
"""

#First FLASK_RESTFUL APP
#from flask import Flask
#from flask_restful import Resource, Api
#
#app = Flask(__name__)
#api = Api(app) 
#
#class Student(Resource):
#    def get(self, name):  ##!! This resource can only be accessed with a GET
#        return {'student': name}
#
#api.add_resource(Student, '/student/<string:name>') #says that student now accessible via API
#
#app.run(port=4998)

### Basic idea looks like the API provides the routing that we saw before, 
## directing requests to resources

###  VIDEO - CREATING THE ITEM RESOURCE ###


#from flask import Flask
#from flask_restful import Resource, Api, request
#
#app = Flask(__name__)
#api = Api(app) 
#
#items = [] # simple in mem DB
#
#class Item(Resource):
#    def get(self, name):  ##!! This resource can only be accessed with a GET
#        item = next(filter(lambda x: x['name'] == name, items), None) # filter returns a filter object!
#        #the wrapper next just gets the first item - for our purposes, since items are unique, only 1!
#        #None is the default
#        return {'item': None}, 404 # this is the failure case, we need it in JSON format!
#                                    # the 404 is a status code!
#    def post(self, name):
#        data = request.get_json()
#        #force=True as param above means we don't need a header, but dangerous
#        #silent just returns none!
#        item = {'name': name, 'price': data['price']}
#        items.append(item)
#        return item, 201  # so caller knows it worked, 201 is successful 
#                          # creation code!!
#
#
#class ItemList(Resource):
#    def get(self):
#        return {'items': items}
#    
#    
#    
#api.add_resource(Item, '/item/<string:name>') #says that student now accessible via API
#api.add_resource(ItemList, '/items')
#app.run(port=4998) # adding the param debug=True gives us rich errors!

from flask import Flask
from flask_restful import Resource, Api, request, reqparse
from flask_jwt import JWT, jwt_required

from Security import authenticate, identity # our file


app = Flask(__name__)
app.secret_key = 'Matt' ### important
api = Api(app) 

jwt = JWT(app, authenticate, identity) ## uses our functions!
## jwt makes a new endpoint, /auth, when we send it a u/p it uses the functions to check
## if it matches, returns a token! The token is then used to 


items = [] # simple in mem DB

class Item(Resource):
    ### !! we put the parser at the class level - so
    ## single PoC
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True)
        
    
    @jwt_required()
    def get(self, name):  ##!! This resource can only be accessed with a GET
        item = next(filter(lambda x: x['name'] == name, items), None) # filter returns a filter object!
        #the wrapper next just gets the first item - for our purposes, since items are unique, only 1!
        #None is the default
        return {'item': item}, 200 if item else 404 # this is the failure case, we need it in JSON format!
                                    # the 404 is a status code!
                                    # Nice use of shortened if statement!
    def post(self, name):
        
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=float, required=True)
        data = parser.parse_args()
        
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': 'an item with name already exists'}, 400
            # this check if the item already exists! 400 is bad request
        
        #data = request.get_json() removed by reqparse
        #force=True as param above means we don't need a header, but dangerous
        #silent just returns none!
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201  # so caller knows it worked, 201 is successful 
                          # creation code!!
    def delete(self, name):
        global items # makes it refer to top level variable!
        items = list(filter(lambda x: x['name'] != name, items))
        # problem here is the aliasing/side effects - I
        # don't like this
        return {'message': 'Item Deleted'}
    
    def put(self, name): # allows us to modify items
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=float, required=True)
        ##this will look at the JSON payload and pull certain
        ## things out - so we can only change price!!!
        ## this is huge - allows us to filter lots of 
        ## nonsense from the json file, and just get what we want
        data = parser.parse_args() # formerly requests.get_json()
        item = next(filter(lambda x : x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {'items': items}
    
    
    
api.add_resource(Item, '/item/<string:name>') #says that student now accessible via API
api.add_resource(ItemList, '/items')
app.run(port=4998) # adding the param debug=True gives us rich errors!

### VIDEO - SECURITY AND AUTHENTICATION -
## we'll use Flask-JWT that provides encrypted JSON
## basically, someone sends us a message, we give them a token to prove they are 
## logged in, then the can send use requests at will
## we'll add a couple useful functions in the file security.py
## PLUS a user class in user.py

### My thoughts: 
# we import key functions from flask and flask-restful
# we create an app, and feed that app to an API - that API will handle many of the wrapping functions
# items is a simple method of storage
# we create an item, and note that it inherits from Resource 
# we create functions for the basic HTTP methods
# # get returns a specific item, in JSON format
# POST starts with a check on existance,
# then creates and appends the item 
# note that we should return the item - helps a lot with debugging
# delete removes everything but - not ideal, but our next version will certainly use SQL 
# note the use of global - handy way to specify the scope
# PUT is like post, but can both update and create
# item list gets everything
