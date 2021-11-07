from __main__ import app
from app import token_required, config_object, Users
from server2_imports import *
from utils import *
'''
Train model on specific column
'''
#TODO: add support for multiple columns
#TODO: fix duplicate projects
#TODO: fix duplicate models
#TODO: only gets model with lowest MSE
#TODO: check whether trained model is already stored before calling train function- hash table to check for membership?
@app.route('/projects/<projname>/models/<column>', methods=['GET', 'POST'])
@token_required
def create_models_single_col(self, projname, column):

    if request.method == 'POST':

        print("starting read")
        df = pd.read_csv(BytesIO(request.files['file'].read()))
        print("done reading")
        df=df.select_dtypes(include=np.number)        
        print("training")
        trained_models = train_models(df, column)
        print("done training")
        client = pymongo.MongoClient(config_object['MONGO']['host'])
        db = client.db

        auth = request.authorization

        user = Users.query.filter_by(name=auth.username).first()

        # db['projects'].insert_one({'name': f'{projname}', 'id': user.public_id})

        # db['projects'].update({'$and':[{'id':user.public_id}, {'name': projname}]},  {'$set': {'models': [{'model-name': key} for key in trained_models]}})

        # db['models'].insert_many([{'projname': projname, 'user_id': user.public_id, 'model-name': key, 'model-data': trained_models[key]} for key in trained_models])

        return '200'
    else:
        client = pymongo.MongoClient(config_object['MONGO']['host'])
        db = client.db

        documents = db[f'{projname}'].find()

        print(documents)

        return '200'
    
'''
Test model on specific column
'''
@app.route('/projects/<projname>/models/<column>/test/', methods=['POST'])
@token_required
def test_models_single_col(self, projname, column):
    
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
            model_list.append([l['model-name'],pickle.loads(l['model-data'])]) #TODO: when to use list and when not to, maybe use hashtable here? 

        tested_models = test_models(model_list, df)
        colname=tested_models[0][0]
        data=tested_models[0][1]
      
        df[colname] = data
        file=df.to_csv()
        # print(df)

        response_stream = BytesIO(file.encode())
        return send_file(
            response_stream,
            mimetype="text/csv",
            attachment_filename="export.csv",
            as_attachment=True
        )

        # return send_file(file, mimetype='text/csv',as_attachment=True, attachment_filename='export.csv')
        # sending raw data as json
        # return jsonify({'results': tested_models})

'''
Test model on all columns
'''
@app.route('/projects/<projname>/models/test/', methods=['POST'])
@token_required
def test_models_all(self, projname):
    
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
            model_list.append([l['model-name'],pickle.loads(l['model-data'])])

        tested_models = test_models(model_list, df)

        # for j in model_list:
            # print(j)
        
        return jsonify({'results': tested_models})

'''
Train model on all columns
'''
@app.route('/projects/<projname>/models/', methods=['GET', 'POST'])
@token_required
def create_models_all(self, projname):

    if request.method == 'POST':

        df = pd.read_csv(BytesIO(request.files['file'].read()))
 
        df=df.select_dtypes(include=np.number)        

        trained_models = train_models(df)

        client = pymongo.MongoClient(config_object['MONGO']['host'])
        db = client.db

        auth = request.authorization

        # user = Users.query.filter_by(name=auth.username).first()

        # db['projects'].insert_one({'name': f'{projname}', 'id': user.public_id})

        # db['projects'].update({'id':user.public_id},  {'$set': {'models': [{'model-name': key} for key in trained_models]}})

        # db['models'].insert_many([{'projname': projname, 'user_id': user.public_id, 'model-name': key, 'model-data': trained_models[key]} for key in trained_models])

        return '200'
    else:
        client = pymongo.MongoClient(config_object['MONGO']['host'])
        db = client.db

        documents = db[f'{projname}'].find()

        print(documents)

        return '200'