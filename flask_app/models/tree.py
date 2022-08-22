from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user


class Trees:
    db = 'Arbortrary'
    def __init__(self,data):
        self.id = data['id']
        self.species = data['species']
        self.location = data['location']
        self.reason = data['reason']
        self.datePlanted = data['datePlanted']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.user_id = data['user_id']
        self.user = None



    @classmethod
    def getAll(cls):
        query = 'SELECT * FROM trees;'
        results = connectToMySQL(cls.db).query_db(query)
        trees = []
        for row in results:
            trees.append(cls(row))
        return trees



    @classmethod
    def getOne(cls, data):
        query = 'SELECT * FROM trees WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])



    @classmethod
    def save(cls, data):
        query = 'INSERT INTO trees (species, location, reason, datePlanted, user_id) VALUES (%(species)s, %(location)s, %(reason)s, %(datePlanted)s, %(user_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)



    @classmethod
    def update(cls, data):
        query = 'UPDATE trees SET species=%(species)s, location=%(location)s, reason=%(reason)s, datePlanted=%(datePlanted)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)



    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM trees WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)



    @classmethod
    def treeUser(cls, data):
        query = 'SELECT * FROM trees LEFT JOIN users ON trees.user_id = user.id WHERE trees.id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        print('treeUser results', results)
        allTrees = []
        for row in results:
            tree = cls(results[0])
            userData = {
                'id': row['user.id'],
                'firstName': row['firstName'],
                'lastName': row['lastName'],
                'email': row['email'],
                'password': row['password'],
                'createdAt': row['user.createdAt'],
                'updatedAt': row['user.updatedAt']
            }
            print('userData model', userData)
            oneUser = user.User(userData)
            tree.user = oneUser
            allTrees.append(tree)
            print('allSightings', allTrees)
        return allTrees
