import re
import requests
import time


# url = "http://127.0.0.1:5000/projects/rivers/models/Total_Revolving_Bal/test/"

# payload={}
# # files=[
# #   ('file',('BankChurners.csv',open('BankChurners.csv','rb'),'text/csv'))
# # ]

# files = {'file': open('BankChurners.csv','rb') }

# headers = {
#   'x-access-tokens': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiI4OTYyMmE5MS1iZmQ4LTQwNDctODRlNS1kYWQ3MWIyZGNiYzEiLCJleHAiOjE2MTE3ODc3MTl9.-n0J3eMh7X2js1fLCuDDnrzLbb6piFuGNX7f4gFzJqI',
#   'Content-Type': 'application/json',
#   'Authorization': 'Basic azpr'
# }

# response = requests.request("POST", url, headers=headers, data=payload, files=files)

# print(response)
# print(type(response))

#------------------

# import requests

# url1 = "http://127.0.0.1:5000/test/parallel?user=1"
# url2= "http://127.0.0.1:5000/test/parallel?user=2"
# # url3= "http://127.0.0.1:5000/test/parallel?user=3"
# # url4= "http://127.0.0.1:5000/test/parallel?user=4"
# # url5= "http://127.0.0.1:5000/test/parallel?user=5"

# payload={}
# headers = {}

# start = time.time()


# response1 = requests.request("GET", url1, headers=headers, data=payload)
# response2 = requests.request("GET", url2, headers=headers, data=payload)
# # response1 = requests.request("GET", url3, headers=headers, data=payload)
# # response2 = requests.request("GET", url4, headers=headers, data=payload)
# # response1 = requests.request("GET", url5, headers=headers, data=payload)

# end = time.time()

# print(end - start)

#-----------------

import grequests

urls = ["http://127.0.0.1:5000/test/parallel?user=1",
"http://127.0.0.1:5000/test/parallel?user=2"]
# "http://127.0.0.1:5000/test/parallel?user=3",
# "http://127.0.0.1:5000/test/parallel?user=4",
# "http://127.0.0.1:5000/test/parallel?user=5"]

rs = (grequests.get(u) for u in urls)

start = time.time()

responses = grequests.map(rs)

end = time.time()

print(end-start)