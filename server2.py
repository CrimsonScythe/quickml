from datetime import datetime
from flask import Flask, json
from flask import request
from flask.helpers import make_response
from flask_cors import CORS, cross_origin
from io import StringIO, BytesIO
import pandas as pd
import numpy as np
from sklearn import linear_model
from flask import Flask, session
from flask import jsonify
from flask_session import Session
import pickle
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
from functools import wraps

app = Flask(__name__)
# app.secret_key = 'Secretkey'

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
def get_all_users():
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
def get_all_projects():

    

    pass


@app.route('/projects/<projname>', methods=['POST'])
@token_required
def create_project(projname):
    pass

@app.route('/projects/<projname>/models/', methods=['GET'])
@token_required
def get_all_models_for_project(projname):
    pass

@app.route('/projects/<projname>/models/<modelname>', methods=['GET'])
@token_required
def get_model_for_project(projname, modelname):
    pass


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
    
#     # print(request.files)
#     # print(request.form)
    
#     # print(request.files['file'].filename)

#     fil = request.files['file']

#     df = pd.read_csv(BytesIO(request.files['file'].read()))
#     col = request.form['column_name']
    
#     reg = linear_model.LinearRegression()

#     df=df.select_dtypes(include=np.number)

#     reg.fit(X=df.drop(columns=[col]), y=df[col])
    

#     with open(f'{fil.filename[:-4]}.pickle', 'wb') as handle:
#         pickle.dump(reg, handle, protocol=pickle.HIGHEST_PROTOCOL)    

#     # reg2 = pickle.loads(s)
#     # preds=reg2.predict(df.drop(columns=[col]))

#     return '200'

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