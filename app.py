from flask import Flask, request, render_template, redirect, url_for
import pymongo
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

# cluster = pymongo.MongoClient(os.environ.get('MONGO_URI'))
cluster = pymongo.MongoClient('localhost')

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')


from user.routes import *

if __name__ == "__main__":
    app.run(threaded = True, port = 8080)