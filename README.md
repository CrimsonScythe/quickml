# quickml
minimal app to quickly and easily train and run ml models
## description
Flask app which runs standard ml models including linear regression, logistic regression, naive bayes and decision trees to create regression models.
Cross validation is used to select the best model.

## tech & deployment

PostgreSQL is used to store user data and serialized scikit models.
Provided CSV data is not stored. It is only persisted locally in memory on the server instance.
The app is dockerized.

## examples & endpoints
Curl request examples for api endpoints are as follows:

#### Register user:
```POST 'http://0.0.0.0:5000/register'```
Pass a JSON object in the body as follows:
```{"name":"a", "password": "a"}```

#### Login user:
```POST 'http://0.0.0.0:5000/login' ```

Choose 'Basic Auth' under Authorization tab in Postman and fill in username and password from earlier.

Returns a JSON web token. Copy and save it for interacting further with the API.

#### Create project and model:
```POST 'http://0.0.0.0:5000/projects/b/models/Dependent_count/train'```

Add 'x-access-tokens' header with value of the token copied earlier.

Add 'Content-type' header with value 'application/json'. 

In the body section:

Add 'file' with value linking to a CSV file.

You can use 'BankChurners.csv' or '5m Sales Records' if you want to test multiprocessing for example.

#### Run prediction using created model:
```POST 'http://0.0.0.0.:5000/projects/b/models/Dependent_count/test/'```

Do same as above.
