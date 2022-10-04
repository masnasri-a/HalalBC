import requests

url = 'http://103.13.206.148:5001/api/v0/add/'
files = {'media': open('requirements.txt', 'rb')}
res = requests.post(url, files=files)
print(res.json())