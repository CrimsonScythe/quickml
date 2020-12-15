from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
from io import StringIO, BytesIO
import pandas as pd

from sklearn import linear_model

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def hello_world():
    print('Hellow works!')
    return 'Hello, World!'

@app.route('/post', methods=['POST'])
def upload():
     
    print(type(request.files['file']))
    

    df = pd.read_csv(BytesIO(request.files['file'].read()))
    
    # runModels(df)

    print(df.head(5))

    return 'Hello World!'

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response

if __name__ == '__main__':
    app.run()

# def runModels(df):
#     reg = linear_model.LinearRegression()
#     reg.fit()