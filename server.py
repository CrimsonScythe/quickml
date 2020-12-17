from flask import Flask, json
from flask import request
from flask_cors import CORS, cross_origin
from io import StringIO, BytesIO
import pandas as pd
import numpy as np
from sklearn import linear_model
from flask import Flask, session
from flask import jsonify
from flask_session import Session
import pickle

app = Flask(__name__)
app.config["DEBUG"] = True
# app.secret_key = 'Secretkey'

SESSION_TYPE = 'filesystem'
SECRET_KEY = 'secretkey'
app.config.from_object(__name__)
Session(app)
CORS(app)



@app.route('/')
def hello_world():
    print('Hellow works!')
    return 'Hello, World!'


@app.route('/post/prep', methods=['POST', 'OPTIONS'])
def upload():
   
    print(request.files['file'])
    df = pd.read_csv(BytesIO(request.files['file'].read()))
    
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    cols = numeric_cols

    return jsonify(cols)

@app.route('/post/train', methods=['POST'])
def trainmodel():
    
    # print(request.files)
    # print(request.form)
    
    # print(request.files['file'].filename)

    fil = request.files['file']

    df = pd.read_csv(BytesIO(request.files['file'].read()))
    col = request.form['column_name']
    
    reg = linear_model.LinearRegression()

    df=df.select_dtypes(include=np.number)

    reg.fit(X=df.drop(columns=[col]), y=df[col])
    

    with open(f'{fil.filename[:-4]}.pickle', 'wb') as handle:
        pickle.dump(reg, handle, protocol=pickle.HIGHEST_PROTOCOL)    

    # reg2 = pickle.loads(s)
    # preds=reg2.predict(df.drop(columns=[col]))

    return '200'

@app.route('/post/pred', methods=['POST'])
def pred():
    
    fil = request.files['file']
    df = pd.read_csv(BytesIO(request.files['file'].read()))

    df=df.select_dtypes(include=np.number)

    col = request.form['column_name']

    with open(f'{fil.filename[:-4]}.pickle', 'rb') as handle:
        res=pickle.load(handle)
    
    ret = res.predict(df.drop(columns=[col]))
    
    print('preds')
    print(ret)

    return jsonify(ret.tolist())

# @app.route('/get/cols', methods=['GET'])
# def getcols():
#     # if request.method == 'OPTIONS':
#     #     resp = Response()
#     #     resp.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:3000/'
#     #     resp.headers['Access-Control-Allow-Credentials'] = True
#     #     resp.headers['Access-Control-Allow-Headers'] = "Content-Type"

#     #     return resp
#     # return '200'
#     print(session['cols'])
#     # print(session.get('cols'))
#     return jsonify(session['cols'])

# @app.after_request
# def after_request(response):
#   response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
#   response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#   response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#   response.headers.add('Access-Control-Allow-Credentials', 'true')
#   return response

if __name__ == '__main__':
    app.run()

# def runModels(df):
#     reg = linear_model.LinearRegression()
#     reg.fit()