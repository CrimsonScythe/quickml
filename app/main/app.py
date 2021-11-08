# from pymongo.common import validate_ok_for_update
import multiprocessing
from server2_imports import *
from models import *
from utils import *
from multiprocessing import Process
# import evaluators

app = Flask(__name__)

'''load config file'''
#TODO: clean this stuff up!
config_object = ConfigParser()
config_object.read('../../config.ini')

app.config['SECRET_KEY']='Th1s1ss3cr3t'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:root@db:5432/quickml2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

queue = multiprocessing.Queue()

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

    collections = Projects.query.with_entities(Projects.name).all()

    if len(collections)==0:
        return 'no projects'
    else:
        return jsonify({'projects': collections})

'''
Get specific model
'''
@app.route('/projects/<projname>/models/<modelname>', methods=['POST'])
@token_required
def find_models(self, projname, modelname):

    model = Models.query.with_entities(Models.data).filter_by(name=modelname, projname=projname).first()
    print(model)
    if model:

        return send_file(
            model,
            mimetype="application/python-pickle",
            attachment_filename="export.pickle",
            as_attachment=True
        )
    
    else:
        return 'No model'


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

        auth = request.authorization

        user = Users.query.filter_by(name=auth.username).first()

        models = Models.query.filter_by(projname=projname, userId=user.public_id).all()
        
        lst = list(models)
        
        for l in lst:
            model_list.append([l.name,pickle.loads(l.data)])  

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


'''
Train model on specific column
'''
#TODO: add support for multiple columns
#TODO: fix duplicate projects
#TODO: fix duplicate models
#TODO: only gets model with lowest MSE
#TODO: check whether trained model is already stored before calling train function- hash table to check for membership?
@app.route('/projects/<projname>/models/<column>/train', methods=['GET', 'POST'])
@token_required
def create_models_single_col(self, projname, column):

    if request.method == 'POST':
        auth = request.authorization
        df = pd.read_csv(BytesIO(request.files['file'].read()))
        df=df.select_dtypes(include=np.number)        

        process = Process(target=train_models, args=(df, queue, column))
        process.start()
        process.join()
        
        trained_models = queue.get()

        user = Users.query.filter_by(name=auth.username).first()

        new_project = Projects(name=projname, user_id=user.public_id)
        db.session.merge(new_project)
        db.session.commit()
        
        db.session.bulk_save_objects([Models(name=key, data=trained_models[key], userId=user.public_id, projname=projname) for key in trained_models])
        db.session.commit()

        return '200'
    else:

        documents = db[f'{projname}'].find()

        print(documents)

        return '200'
    

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)

