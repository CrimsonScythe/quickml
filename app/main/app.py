from pymongo.common import validate_ok_for_update
from server2_imports import *

app = Flask(__name__)

import models

'''load config file'''
config_object = ConfigParser()
config_object.read('../../config.ini')

app.config['SECRET_KEY']='Th1s1ss3cr3t'
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///C:/Users/hasee/Downloads/sqlite-tools-win32-x86-3340000/sqlite-tools-win32-x86-3340000.library.db'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgres@localhost:5432/quickml2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

'''
User data model
'''
class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    admin = db.Column(db.Boolean)

    def __init__(self, id, public_id, name, password, admin):
        self.id = id
        self.public_id = public_id
        self.name = name
        self.password = password
        self.admin = admin

    def __repr__(self):
        return f"<User {self.name}>"




# db.create_all()

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
    client = pymongo.MongoClient(config_object['MONGO']['host'])
    db = client.db

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

    client = pymongo.MongoClient(config_object['MONGO']['host'])
    db = client.db

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
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)


