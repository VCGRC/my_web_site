from quart import Quart, request, render_template, redirect, url_for
from motor.motor_tornado import MotorClient
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

app = Quart(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

# cluster = pymongo.MongoClient(os.environ.get('MONGO_URI'))
cluster = MotorClient('localhost')

@app.route('/', methods = ['GET'])
async def index():
    return await render_template('index.html')
    


from user.routes import *
from bot_api.routes import *

if __name__ == "__main__":
    app.run(threaded = True, port = 8080)