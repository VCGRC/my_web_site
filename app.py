from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
import pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv, find_dotenv
import datetime
import uvicorn
load_dotenv(find_dotenv())

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# cluster = pymongo.MongoClient(os.environ.get('MONGO_URI'))
cluster = MongoClient('localhost')

# @app.route('/', methods = ['GET'])
# async def index():
#     news_collection = cluster.web.news
#     news = news_collection.find().sort('create_date', pymongo.DESCENDING).limit(10)
#     return await render_template('index.html', news = news)

# @app.route('/create_news/', methods = ['GET', 'POST'])
# async def create_news():
#     if request.method == 'GET':
#         return await render_template('create_news.html')

#     if request.method == 'POST':

#         news_collection = cluster.web.news
#         data = await request.form
#         record = {
#             'create_date':datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
#             'text':data['text'],
#             'title':data['title']
#         }

#         news_collection.insert_one(record)
#         return redirect('/')
    
@app.get('/api/v1/news/get')
async def get_news(request:Request):
    news_collection = cluster.web.news
    news = news_collection.find().sort('create_date', pymongo.DESCENDING).limit(10)
    print('Привет мир')
    list_of_news = []
    for new in news:
        list_of_news.append({'title':new['title'], 'create_date':new['create_date'], 'text':new['text'], '_id':new['_id']})
        # print({'title':new['title'], 'create_date':new['create_date'], 'text':new['text'], '_id':new['_id']})
    return list_of_news

# from user.routes import *
from bot_api.routes import *

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port = 8080)