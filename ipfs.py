import ipfsapi

try:
    api = ipfsapi.connect('103.13.206.148', 5001)
    print(api)
except ipfsapi.exceptions.ConnectionError as ce:
    print(str(ce))
