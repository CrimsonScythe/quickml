from server2_imports import *

db = SQLAlchemy()

'''
User data model
'''
class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.Text, unique=True)
    name = db.Column(db.Text)
    password = db.Column(db.Text)
    admin = db.Column(db.Boolean)
    projects = db.relationship('Projects')
    models = db.relationship('Models')

    def __init__(self, public_id, name, password, admin):
        self.public_id = public_id
        self.name = name
        self.password = password
        self.admin = admin

    def __repr__(self):
        return f"<User {self.name}>"

'''
Projects data model
'''
class Projects(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    user_id = db.Column(db.Text, db.ForeignKey('users.public_id'))

    # models = db.relationship('Models')

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    def __repr__(self):
        return f"<Project {self.name}>"

'''
Models data model
'''
class Models(db.Model):
    __tablename__ = 'models'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), primary_key=True)
    data = db.Column(db.LargeBinary)
    userId = db.Column(db.Text, db.ForeignKey('users.public_id'))
    projname = db.Column(db.String(50))
    # projname = db.Column(db.String(50), db.ForeignKey('projects.name'))
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, data, userId, projname):
        self.name = name
        self.data = data
        self.userId = userId
        self.projname = projname

    def __repr__(self):
        return f"<Models {self.name}>"