from pymongo import MongoClient

# configure/initialize database
# see: https://pymongo.readthedocs.io/en/stable/examples/authentication.html
uri = 'mongodb+srv://bl275:<password>@cluster0.lyqc4ch.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(uri)
database = client.discrete_exchange