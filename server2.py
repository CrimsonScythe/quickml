import datetime
from flask import Flask, json
from flask import request
from flask.helpers import make_response
from pymongo.common import validate_document_class
from flask_cors import CORS, cross_origin
from io import StringIO, BytesIO
import pandas as pd
import numpy as np
from sklearn import linear_model, svm
from sklearn.neighbors import KNeighborsRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn import tree
from flask import Flask, session
from flask import jsonify
from flask_session import Session
import pickle
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import pymongo
from functools import wraps
from configparser import ConfigParser

app = Flask(__name__)
# app.secret_key = 'Secretkey'

'''load config file'''
config_object = ConfigParser()
config_object.read('config.ini')

app.config['SECRET_KEY']='Th1s1ss3cr3t'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///C:/Users/hasee/Downloads/sqlite-tools-win32-x86-3340000/sqlite-tools-win32-x86-3340000.library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    admin = db.Column(db.Boolean)

CORS(app)

# db.create_all()

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = Users.query.filter_by(public_id = data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})            

        return f(current_user, *args, **kwargs)
    return decorator

@app.route('/register', methods=['GET', 'POST'])
def signup_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')
    
    new_user = Users(public_id = str(uuid.uuid4()), name = data['name'], password= hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'registered successfully'})


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    user = Users.query.filter_by(name=auth.username).first()

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])  
        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})


@app.route('/users', methods=['GET'])
@token_required
def get_all_users(self):
    users = Users.query.all()
    result=[]

    for user in users:
        user_data = {}
        user_data['public_id']=user.public_id
        user_data['name']=user.name
        user_data['password']=user.password
        user_data['admin']=user.admin

        result.append(user_data)

    return jsonify({'users': result})

@app.route('/projects/', methods=['GET'])
@token_required
def get_all_projects(self):
    client = pymongo.MongoClient(config_object['MONGO']['host'])
    db = client.db

    collections = db.list_collection_names()

    if len(collections)==0:
        return 'no projects'
    else:
        return jsonify({'projects': collections})

# def test_models(df, models, column=None):
#     if column:
    

        
#     else:
#         pass


def train_models(df, column=None):

    if column:
        trained_models={}

        models={
            'linear': linear_model.LinearRegression(),
            'svm': svm.SVR(),
            'nn': KNeighborsRegressor(),
            # 'dt': tree.DecisionTreeClassifier()
        }

        for name, model in models.items():
            trained_models[f'{column}-{name}']=pickle.dumps(model.fit(df.drop(columns=[column]), df[column]))


        return trained_models

    else:

        trained_models={}

        models={
            'linear': linear_model.LinearRegression(),
            'svm': svm.SVR(),
            'nn': KNeighborsRegressor()
            # 'gpr': GaussianProcessRegressor(),
            # 'dt': tree.DecisionTreeClassifier()
        }

        for column in df.columns:
            for name, model in models.items():
                trained_models[f'{column}-{name}'] = pickle.dumps(model.fit(df.drop(columns=[column]),df[column]))

        return trained_models

@app.route('/project/<projname>/models/<column>', methods=['GET', 'POST'])
@token_required
def get_create_single_models(self, projname, column):
    if request.method == 'POST':
        df = pd.read_csv(BytesIO(request.files['file'].read()))
        
        df = df.select_dtypes(include=np.number)

        trained_models = train_models(df, column)

        client = pymongo.MongoClient(config_object['MONGO']['host'])
        db = client.db

        

        documents = db[f'{projname}'].insert_many([{'model-data': trained_models[key]} for key in trained_models])

        return '200'

    else:
        pass
    

@app.route('/projects/<projname>/models/test/', methods=['GET', 'POST'])
@token_required
def get_test_models_all(self, projname):
    
    if request.method == 'POST':

        model_list = []

        df = pd.read_csv(BytesIO(request.files['file'].read()))
        df = df.select_dtypes(include=np.number)

        client = pymongo.MongoClient(config_object['MONGO']['host'])
        db = client.db

        auth = request.authorization

        user = Users.query.filter_by(name=auth.username).first()

        models = db['models'].find({'$and': [{'user_id': user.public_id},{'projname': projname}]})

        lst = list(models)
        for l in lst:
            # print(l['model-name'])
            # print(type(l))
            model_list.append(pickle.loads(l['model-data']))

        # tested_models = test_models(models, df)
        for j in model_list:
            print(j)

    return '200'

@app.route('/projects/<projname>/models/', methods=['GET', 'POST'])
@token_required
def get_create_models(self, projname):

    if request.method == 'POST':

        df = pd.read_csv(BytesIO(request.files['file'].read()))
 
        df=df.select_dtypes(include=np.number)        

        trained_models = train_models(df)

        client = pymongo.MongoClient(config_object['MONGO']['host'])
        db = client.db

        auth = request.authorization

        user = Users.query.filter_by(name=auth.username).first()

        db['projects'].insert_one({'name': f'{projname}', 'id': user.public_id})

        # db['projects'].find({'id': user.public_id})[f'{}']

        db['projects'].update({'id':user.public_id},  {'$set': {'models': [{'model-name': key} for key in trained_models]}})

        db['models'].insert_many([{'projname': projname, 'user_id': user.public_id, 'model-name': key, 'model-data': trained_models[key]} for key in trained_models])


        # db['projects'].update({'id':user.public_id},  {'models': [{'model-name': key, 'model-data': trained_models[key]} for key in trained_models]})

        # documents = db['projects'].insert_many([{'model-name': key, 'model-data': trained_models[key]} for key in trained_models])

        return '200'
    else:
        client = pymongo.MongoClient(config_object['MONGO']['host'])
        db = client.db

        documents = db[f'{projname}'].find()

        print(documents)

        return '200'
        # if documents.count==0:
        #     return 'No models'
        # else:
        #     jsonify({'models': documents})

@app.route('/projects/<projname>/models/<modelname>', methods=['GET'])
@token_required
def test_models(projname, modelname):

    client = pymongo.MongoClient(config_object['MONGO']['host'])
    db = client.db

    model = db['projects'].find({'$and': [{'models': modelname},{"name": f"{projname}"}]})

    # model = db[f'{projname}'].find({"name": f"{modelname}"})

    if model:
        return jsonify({"model": model})
    else:
        return 'No model'


if __name__ == '__main__':
    app.run(debug=True)


    # @app.route('/post/prep', methods=['POST', 'OPTIONS'])
# def upload():
   
#     print(request.files['file'])
#     df = pd.read_csv(BytesIO(request.files['file'].read()))
    
#     numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
#     cols = numeric_cols

#     return jsonify(cols)

# @app.route('/post/train', methods=['POST'])
# def trainmodel():
    
    # # print(request.files)
    # # print(request.form)
    
    # # print(request.files['file'].filename)

    # fil = request.files['file']

    # df = pd.read_csv(BytesIO(request.files['file'].read()))
    # col = request.form['column_name']
    
    # reg = linear_model.LinearRegression()

    # df=df.select_dtypes(include=np.number)

    # reg.fit(X=df.drop(columns=[col]), y=df[col])
    

    # with open(f'{fil.filename[:-4]}.pickle', 'wb') as handle:
    #     pickle.dump(reg, handle, protocol=pickle.HIGHEST_PROTOCOL)    

    # # reg2 = pickle.loads(s)
    # # preds=reg2.predict(df.drop(columns=[col]))

    # return '200'

# @app.route('/post/pred', methods=['POST'])
# def pred():
    
#     fil = request.files['file']
#     df = pd.read_csv(BytesIO(request.files['file'].read()))

#     df=df.select_dtypes(include=np.number)

#     col = request.form['column_name']

#     with open(f'{fil.filename[:-4]}.pickle', 'rb') as handle:
#         res=pickle.load(handle)
    
#     ret = res.predict(df.drop(columns=[col]))
    
#     print('preds')
#     print(ret)

#     return jsonify(ret.tolist())

# # @app.route('/get/cols', methods=['GET'])
# # def getcols():
# #     # if request.method == 'OPTIONS':
# #     #     resp = Response()
# #     #     resp.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:3000/'
# #     #     resp.headers['Access-Control-Allow-Credentials'] = True
# #     #     resp.headers['Access-Control-Allow-Headers'] = "Content-Type"

# #     #     return resp
# #     # return '200'
# #     print(session['cols'])
# #     # print(session.get('cols'))
# #     return jsonify(session['cols'])

# # @app.after_request
# # def after_request(response):
# #   response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
# #   response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
# #   response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
# #   response.headers.add('Access-Control-Allow-Credentials', 'true')
# #   return response

# if __name__ == '__main__':
#     app.run()

# # def runModels(df):
# #     reg = linear_model.LinearRegression()
# #     reg.fit()