from server2_imports import *

'''
Helper method for model training
'''
def train_models(df, queue, column=None):

    
    if column:
        print("column")
        # train test split for cross val
        X_train, X_test, y_train, y_test = train_test_split(df.drop(columns=[column]), df[column], test_size=0.33)

        trained_models={}
        validated_models={}

        models={
            'linear': linear_model.LinearRegression(),
            # 'svm': svm.SVR(),
            # 'nn': KNeighborsRegressor(),
            # 'dt': tree.DecisionTreeClassifier()
        }

        for name, model in models.items():
            print("fitting")
            md = model.fit(X_train, y_train)
            print("pred")
            y_pred = md.predict(X_test)
            mse=mean_squared_error(y_test, y_pred)
            print("validated")
            validated_models[mse]=[f'{column}-{name}', pickle.dumps(md)]

        # get model with lowest mse
        trained_models[validated_models[min(validated_models)][0]] = validated_models[min(validated_models)][1]
        
        queue.put(trained_models)
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

'''
Helper method for model inference
'''
def test_models(model_list, df):
    results=[]
    for model in model_list:
        
        
        results.append([model[0].split('-')[0],model[1].predict(df.drop(columns=[model[0].split('-')[0]])).tolist()]) #TODO: break up into smaller chunks

    return results
