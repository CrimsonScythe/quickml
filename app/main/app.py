# from pymongo.common import validate_ok_for_update
from server2_imports import *
from models import *
from utils import *
# import evaluators

app = Flask(__name__)

'''load config file'''
config_object = ConfigParser()
config_object.read('../../config.ini')

app.config['SECRET_KEY']='Th1s1ss3cr3t'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:root@localhost:5432/quickml2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# if __name__ == '__main__':

# app.run(debug=True)

'''
Decorator function for authentication
'''
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

'''
Register user
'''
@app.route('/register', methods=['GET', 'POST'])
def signup_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')
    
    new_user = Users(public_id = str(uuid.uuid4()), name = data['name'], password= hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'registered successfully'})

'''
Sign in user
'''
@app.route('/login', methods=['GET', 'POST'])
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    user = Users.query.filter_by(name=auth.username).first()
    
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=30)}, app.config['SECRET_KEY'])  
        print(type(token))
        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

'''
Get list of all users
'''
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

    

'''
Get list of all projects
'''
@app.route('/projects/', methods=['GET'])
@token_required
def get_all_projects(self):
    # client = pymongo.MongoClient(config_object['MONGO']['host'])
    # db = client.db

    collections = db.list_collection_names()

    if len(collections)==0:
        return 'no projects'
    else:
        return jsonify({'projects': collections})

'''
Get specific model
'''
@app.route('/projects/<projname>/models/<modelname>', methods=['GET'])
@token_required
def find_models(projname, modelname):

    # client = pymongo.MongoClient(config_object['MONGO']['host'])
    # db = client.db

    model = db['projects'].find({'$and': [{'models': modelname},{"name": f"{projname}"}]})

    # model = db[f'{projname}'].find({"name": f"{modelname}"})

    if model:
        return jsonify({"model": model})
    else:
        return 'No model'


@app.route('/test/parallel', methods=['GET'])
def test_parallel():
    a=1 
    print(f'Serving client {request.args.get("user")}')
    while(a < 1000000000):
        a+=1
    print(f'finished client {request.args.get("user")}')
    return '200'

#############


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
        

        # client = pymongo.MongoClient(config_object['MONGO']['host'])
        # db = client.db

        auth = request.authorization

        user = Users.query.filter_by(name=auth.username).first()

        models = Models.query.filter_by(projname=projname, userId=user.public_id).all()
        print(models)
        # models = db['models'].find({'$and': [{'user_id': user.public_id},{'projname': projname}]})
        
        print('getting list')
        lst = list(models)
        print('list is')
        print(lst)
        for l in lst:
            # print(l['name'])
            model_list.append([l.name,pickle.loads(l.data)]) #TODO: when to use list and when not to, maybe use hashtable here? 

        tested_models = test_models(model_list, df)
        colname=tested_models[0][0]
        data=tested_models[0][1]
      
        df[colname] = data
        file=df.to_csv()

        response_stream = BytesIO(file.encode())
        return send_file(
            response_stream,
            mimetype="text/csv",
            attachment_filename="export.csv",
            as_attachment=True
        )

        return '200'


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
        # client = pymongo.MongoClient(config_object['MONGO']['host'])
        # db = client.db

        auth = request.authorization

        user = Users.query.filter_by(name=auth.username).first()

        new_project = Projects(name=projname, user_id=user.public_id)
        db.session.merge(new_project)
        db.session.commit()
        
        db.session.bulk_save_objects([Models(name=key, data=trained_models[key], userId=user.public_id, projname=projname) for key in trained_models])
        db.session.commit()
        # db['projects'].insert_one({'name': f'{projname}', 'id': user.public_id})

        # db['projects'].update({'$and':[{'id':user.public_id}, {'name': projname}]},  {'$set': {'models': [{'model-name': key} for key in trained_models]}})

        # db['models'].insert_many([{'projname': projname, 'user_id': user.public_id, 'model-name': key, 'model-data': trained_models[key]} for key in trained_models])

        return '200'
    else:
        # client = pymongo.MongoClient(config_object['MONGO']['host'])
        # db = client.db

        documents = db[f'{projname}'].find()

        print(documents)

        return '200'
    
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

        # client = pymongo.MongoClient(config_object['MONGO']['host'])
        # db = client.db

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

        # client = pymongo.MongoClient(config_object['MONGO']['host'])
        # db = client.db

        auth = request.authorization

        # user = Users.query.filter_by(name=auth.username).first()

        # db['projects'].insert_one({'name': f'{projname}', 'id': user.public_id})

        # db['projects'].update({'id':user.public_id},  {'$set': {'models': [{'model-name': key} for key in trained_models]}})

        # db['models'].insert_many([{'projname': projname, 'user_id': user.public_id, 'model-name': key, 'model-data': trained_models[key]} for key in trained_models])

        return '200'
    else:
        # client = pymongo.MongoClient(config_object['MONGO']['host'])
        # db = client.db

        documents = db[f'{projname}'].find()

        print(documents)

        return '200'

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)

