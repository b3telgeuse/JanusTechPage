from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_app.models import tree


class User:
    db = 'janusII'
    def __init__(self, data):
        self.id = data['id']
        self.firstName = data['firstName']
        self.lastName = data['lastName']
        self.email = data['email']
        self.password = data['password']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.sightings = []



    @classmethod
    def getAll(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users



    @classmethod
    def getOne(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])



    @classmethod
    def getEmail(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])



    @classmethod
    def save(cls, data):
        query = 'INSERT INTO users (firstName, lastName, email, password) VALUES (%(firstName)s, %(lastName)s, %(email)s, %(password)s);'
        return connectToMySQL(cls.db).query_db(query, data)



    @classmethod
    def update(cls, data):
        query = 'UPDATE users SET firstName=%(firstName)s, lastName=%(lastName)s, email=%(email)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)



    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM users WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)



    def fullName(self):
        return f'{self.firstName} {self.lastName}'



    @staticmethod
    def validate(user):
        isValid = True
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(User.db).query_db(query, user)
        if len(results) >= 1:
            isValid = False
            flash("That email is already in our system")
        if not EMAIL_REGEX.match(user['email']):
            isValid = False
            flash("Invalid Email format")
        if len(user['firstName']) < 2:
            isValid = False
            flash("First Name must have at least 2 characters")
        if len(user['lastName']) < 2:
            isValid = False
            flash("Last Name must have at least 2 characters")
        if len(user['password']) < 2:
            isValid = False
            flash("Password must have at least 2 characters")
        if user['password'] != user['confirm']:
            isValid = False
            flash("Passwords are not matching")
        return isValid

