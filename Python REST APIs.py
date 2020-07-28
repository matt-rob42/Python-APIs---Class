# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 20:12:34 2020

@author: matt_
"""
###UDEMY REST APIs with Python

###We'll start with some review material - some of this stuff is quite nice

###Dictionary comprehension 

#users = [(0, 'Bob', 'abc123')]  ###This is our underlying list of user info tuples
#
#User_mapping = {user[1]: user for user in users}  ###This is the dict comprehension, makes the username the key
#
#
#Username_input = input("Enter U")
#Password_input = input("Enter P")
#
#_, username, password = User_mapping[Username_input]  ###This is a nice unpacking, note the blank var

####################################################

###Unpacking function arguments

#def multiply(*args):###star is key args are anything
#    print(args)     ###args is just a placeholder for
#    total = 1               ###as many vars as we want!
#    for arg in args:
#        total = total * arg
#    return total
#
####This allows us to collect multiple (arbitrary?)
####number of args we might want to input
####Countless uses
#
####!!!We can also do this in reverse - unpack a list 
####so that we can use its elements
####one value per param
#def add(x,y):
#    return x+y
#
#nums = [3,5]
#print(add(*nums))
#
####We can also do this with named args: #This is specifically for dictionaries! i.e. **
#nums = {"x":15, "y":25}
#print(add(**nums))
#
###This passes each key as an argument! With value that is associated with
####The key!
#
####We also can use the operator param - as before, we can pass n
####params with *args - but at the end we must also pass a named param
#
#def apply(*args, operator):
#    if operator == "*":
#        return multiply(*args)
#    elif operator == "+":
#        return sum(args)
#    else:
#        return "lol"
#print(apply(1,2,3,  operator = "*")) #Remove star before args in mult!

########################################################### OOP ###############
#student = {"name": "Matt", "grades":(89,90,93,78,90)}
#
#def average(sequence):
#    return sum(sequence)/len(sequence)
#
#print(average(student["grades"]))

###Simple enough, but we want an object that can support all these
###functions and data

###Here, we define a class, that has attributes, like name
###that we can access using self
class Student(object):
    def __init__(self, name, grades):          ###to instantiate fn (method)
        self.name =name
        self.grades = grades ### this both creates and sets name property
    def average(self):     ###Self is the parameter!!
        return sum(self.grades)/len(self.grades)



###Test 1        
#student = Student("Matt", (100,90))
#print(student.name)
#print(student.average())
        
###Now, let's look at more special methods (AKA "Magic"):
        
class Person(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age
###Now if we instantiate this, we get a person
### bob = Person("Bob", 35)
###print(bob) just gives a meaningless string
###So how do we print something useful?
###Using f-string
        
    def __str__(self):
        return f"Person {self.name}, {self.age} years old."
    
###We also have a __repr__ method, that should give us enough info to 
###recreate the object, <> imply object
    def __repr__(self):
        return f"<Person ('{self.name}', {self.age}) years old.>"
    
    
###Class Methods and Static Methods#############

class ClassTest(object):
    def instance_method(self):
        print(f"Called instance_method of {self}")
        
    @classmethod
    def class_method(cls):
        print(f"Called class_method of {cls}")
    
    @staticmethod
    def static_method():
        print("Called static method")
        
### what are these used for? Instance are basically normal methods, 
###using the data of the class
###classmethods are "factories" see below
###Static methods are just to put a method in a class?

###We can also give classes variable/properties/attributes!!!!!!
class Book(object):
    TYPES = ("hardcover", "paperback")  
    
    def __init__(self, name, book_type, weight):
        self.name = name
        self.book_type = book_type
        self.weight = weight

###!!!We want some way to limit our instantiation
### to have book type from only TYPES
    @classmethod
    def hardcover(cls, name, page_weight):
        return Book(name, Book.TYPES[0], page_weight + 100)
   
###So now we can create hardcover books! This is what it means by factory
    @classmethod 
    def paperback(cls, name, page_weight): ##cls is the class, sort of like calling self
        return Book(name, Book.TYPES[1], page_weight)
    
    
book = Book.hardcover("HP", 1500)        
book2 = Book.paperback("ddd", 1222)   
#test = ClassTest()
##test.instance_method()
#ClassTest.class_method()

### inheritance ###################################
### We'll use device as a basic class to build on
class Device(object):
    def __init__(self, name, connected_by):
        self.name = name
        self.connected_by = connected_by
        self.connected = True
    def __str__(self):
        return f"Device {self.name!r} ({self.connected_by})"
    
    def disconnect(self):
        self.connected = False
        print("Disconnected.")
###Now we'll create another class that EXTENDS this one
class Printer(Device):
    def __init__(self, name, connected_by, capacity):
        super().__init__(name, connected_by)
        self.capacity = capacity
        self.remaining_pages = capacity
    def __str__(self):
        return f"{super().__str__()} ({self.remaining_pages} pages remaining)"
    def print(self, pages):
        if not self.connected:
            print("Not conn")
        self.remaining_pages -= pages
printer = Printer("kkp", "frg", 23) 

###!!! This printer has its own methods, but can still access parent methods!
####NOTES - CLASS COMPOSITION BIG IDEA
#Below, old
#class Bookshelf:
#    def __init__(self,quantity):
#        self.quantity = quantity
#    
#    def __str__(self):
#        return f"Bookshelf with {self.quantity} books"
#Here's V2
class Bookshelf:
    def __init__(self, *books):
        self.books = books
    
    def __str__(self):
        return f"Bookshelf with {len(self.books)} books"
###Now, say we wanted to make a class called Book - we might be
###tempted to make it inherit from bookshelf
#Below, OLD
#class Book(Bookshelf):
#    def __init__(self, name, quantity) #This is where the issues 
#    #begin, we need quantity to call the super's init, but this might 
#    #not be relevant for books
#    super().__init__(quantity)
#    self.name = name
#    #Next problem - if we try to print it, it will use print from super
#    #this is wrong, so we'll have to override with a new __str__
#    #method - more work

#Here's V2
        
class Book:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return f"Book {self.name}"
    
    
#So, here's a better idea - see above
book = Book("Harry Potter")
book2 = Book("P 101")
shelf = Bookshelf(book, book2)
#print(shelf)
###!!!!!!This is much more common than inher, model it as a class that
### contains other classes - but they are not nec. decendants

###Lecture - Type Hinting

from typing import List

def list_avg(sequence: List) -> float: # tells us var should be a list!
    return sum(sequence)/len(sequence)

#eg
class Bookshelf:
    def __init__(self, books: List[Book]):
        self.books = books
    
    def __str__(self) -> str:
        return f"Bookshelf with {len(self.books)} books"

###Imports in Python:#################

# We want to be able to import code from one module to another
#from ImportTest import divide

#print(divide(10,2))

# ? How does Python know where the other files are?

import sys

#print(sys.path)

# shows us all the paths we might want

#print(sys.modules) tells us all modules in use!!!

### VIDEO -  ERRORS ###

#def divide(dividend, divisor):
#    if divisor == 0:
#        print("mmmmm")
#        return
#    return dividend/divisor

### This program has an obvious possible divide by 0 error
### So how to overcome this? Errors for flow control
    
#def divide(dividend, divisor):
#    if divisor == 0:
#        raise ZeroDivisionError("Can't be 0") #raises spec error plus a message
#    return dividend/divisor


### At the calling level, we use the try/except/else blocks to capture errors
### and trigger some control flow
    
### Writing our own error types ###

# we need to define the error class:
class TooManyPagesError(ValueError): # We either inherit from the general 
    #Exception class, or a specific error class
    pass

class Book:
    def __init__(self, name, page_count):
        self.name = name
        self.page_count = page_count
        self.pages_read = 0
    def __repr__(self):
        return ("")
    
    def read(self, pages):
        if self.pages_read + pages > self.page_count:
            raise TooManyPagesError("Oops")   # this is our error class!
            
            
        self.pages_read += pages
        print("")


# but, what if we read more pages than in the book???
        
### VIDEO - First Class Functions ###
        
#functions as variables
#def divide(dividend, divisor):
#    if divisor == 0:
#        raise ZeroDivisionError("Can't be 0") #raises spec error plus a message
#    return dividend/divisor
#
#def calculate(*values, operator): # any num of args
#    return operator(*values)      # operates on it
#
#result = calculate(20, 4, operator = divide) #func itself, not a fn call
##print(result)
#
#
#def search(sequence, expected, finder):
#    for elem in sequence:
#        if finder == expected:
#            return elem
#    raise RunTimeError
#
#def get_friend_name(friend):
#    return friend["name"]

###### SIMPLE DECORATORS ######
# Say we wanted a way to control how someone could use thefollowing function:
        
user = {"usernme": "jose", "access_level":"admin"} 

#def get_admin_password():
#    return "12345"

# So how to control access? we could do this:
#if user["access_level"] == "admin":
#    print(get_admin_password())
    

# But the function itself is still insecure - we could try this:
# embedding the check in the fn
    
def secure_get_admin():
    if user["access_level"] == "admin":
        print(get_admin_password())
### A decorator allows us to mod the fn without adding this extra line
### to everything!
    
def secure_function(func):
    if user["access_level"] == "admin":
        return func
#This is how we'd do this
#get_admin_password = secure_function(get_admin_password())
#BUT This requires that user is an admin before we secure the fn
#We want to check the access level when we call it, not when we define it
def make_secure(func):
    def secure_function():
        if user["access_level"] == "admin":
            return func() #returns a function call!!!
        
    return secure_function

# This allows us to return a function if the permissions are correct
# actual fn, not just the call need to review this
    
### VIDEO - THE @ SYNTAX FOR DECORATORS ########
# Here the decorator is a call to our previously defined make_secure function 
    
@make_secure
def get_admin_password():
    return "12345"
  

print(get_admin_password())

# This is pretty cool, g_a_p triggers make_secure I believe passing
# g_a_p as its func parameter

### functools wraps - need to research 

#### VIDEO dec fns with params

## NEED TO REVIEW THIS LATER...

#### UNIT 3 - FIRST REST API

### See related file: app.py

#### VIDEO - HTTP VERBS ####

### What is a web server? 
### blend of software designed to respond to incoming requests
### what do we send when we "hit" a URL? 
### for example, http://www.google.com
### we send GET/HTTP/1.1
## GET is a verb, what we want to return
## / is a path (location?)
## http version
## server can return many things, errors, data etc.
## going to web page will always be a GET
## we can also do POST, DELETE, PUT etc.

### VIDEO - REST PRINCIPLES ####

## we know going to a site performs a GET
## other things are possible
## REST API uses this to serve up data
## REST is a way of thinking about how a web server behaves 

## Doesn't respond with just data - instead RESOURCES
## Things (objects) that the server has
## Imagine server can take GET/item/chair, and POST/item/chair + data to make new chair
## also PUT/item/chair + data, and DELETE/item/chair
## these all have the same / locations, because they all are accessing the 
## same resources 
## REST is stateless!!! just means that one request cannot 
## depend on other requests
## e.g. we use POST to create a chair, server doesn't "know" the item exists
## it is stored in DB
## when we want to extract it, the server still knows nothing - it must check the DB
## SO GET DOESN"T RELY ON POST
## e.g. user logs into web app, recieves some unique data
## server does not know this, as it has no state
## user must send auth data every time they interact
## VIDEO CREATING ENDPOINTS - SEE app.py ###

## VIDEO - TESTING ENDPOITS WITH POSTMAN!!!

### VIDEO - VIRTUAL ENVs and FLASK - RESTFUL ###

## This will be a full rest API, using a library extension 
## see the file called app2.py

### VIDEO - TEST FIRST API DESIGN ###

## go to postman, call it section 4, we need to get test cases clear to get endpoints 
## clear!

## imagine an API dealing with items, what might we need?
## get all items,

