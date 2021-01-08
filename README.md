# quickml
minimal app to quickly and easily train and run ml models
## description
Flask app which runs standard ml models including linear regression, logistic regression, naive bayes and decision trees to create regression models.
Cross validation is used to select the best model.

## tech & deployment
MongoDB Atlas is used to store models. User data is stored locally using SQLite3.
The provided data is not stored on any database. It is only persisted locally in memory on the server instance.
The app is dockerized and deployed on AWS EC2 instance.

## examples & endpoints
Curl request examples for api endpoints are as follows:

Register user:
```
curl --location --request GET 'http://18.191.11.7:5000/register' \
--header 'Content-Type: application/json' \
--data-raw '{"name":"lama", "password": "lama"}'
```

Login user:
```
curl --location --request GET 'http://18.191.11.7:5000/login' \
--header 'Authorization: Basic bGFtYTpsYW1h' \
--data-raw ''
```

Create project and model:
```
curl --location --request POST 'http://18.191.11.7:5000/projects/lama/models/Dependent_count' \
--header 'x-access-tokens: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJlNzJhMzlmYi0yM2NjLTQ4M2QtYjA1Mi05NTY5YTkwNWMwYjEiLCJleHAiOjE2MTIzOTA3ODd9.4lZQ1X8-2BL_IRcFDO5ODIH1gGKXaEPF6zL9PdLKxYY' \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic bGFtYTpsYW1h' \
--form 'file=@"/path/to/BankChurners.csv"'
```

Run prediction using created model:
```
curl --location --request POST 'http://18.191.11.7:5000/projects/lama/models/Dependent_count/test/' \
--header 'x-access-tokens: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJlNzJhMzlmYi0yM2NjLTQ4M2QtYjA1Mi05NTY5YTkwNWMwYjEiLCJleHAiOjE2MTIzOTA3ODd9.4lZQ1X8-2BL_IRcFDO5ODIH1gGKXaEPF6zL9PdLKxYY' \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic bGFtYTpsYW1h' \
--form 'file=@"/path/to/BankChurners.csv"'
```
## Postman button 
You can also use the button which invokes the model create and prediction endpoints above using an already logged in user:

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/af340f6e9202084237b9)
