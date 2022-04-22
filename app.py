from uuid import uuid4
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
import pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv, find_dotenv
import datetime
import uvicorn
from pydantic import BaseModel
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

class Article(BaseModel):
    text: str
    title: str

@app.post('/api/v1/news/create')
async def create_new(article:Article):
    news_collection = cluster.web.news
    record = {
        '_id':uuid4().hex,
        'create_date':datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        'text':article.text,
        'title':article.title
    }
    try:
        res = news_collection.insert_one(record)
        return {'result':'success', '_id':str(res.inserted_id)}
    except Exception as e:
        return {'result':'error', 'error':str(e)}

@app.delete('/api/v1/news/delete/<_id>')
async def delete_new(_id, request:Request):
    news_collection = cluster.web.news
    try:
        new = news_collection.delete_one({'_id':_id})
        return {'result':'success'}
    except Exception as e:
        return {'result':'error', 'error':str(e)}

@app.get('/api/v1/news/get/<_id>')
async def get_one_new(_id, request:Request):
    news_collection = cluster.web.news
    new = news_collection.find_one({'_id':_id})
    data = {'title':new['title'], 'create_date':new['create_date'], 'text':new['text'], '_id':str(new['_id'])}
    return data
    
@app.get('/api/v1/news/get')
async def get_news(request:Request):
    news_collection = cluster.web.news
    news = news_collection.find().sort('create_date', pymongo.DESCENDING).limit(10)
    list_of_news = []
    for new in news:
        list_of_news.append({'title':new['title'], 'create_date':new['create_date'], 'text':new['text'], '_id':str(new['_id'])})
    return list_of_news

@app.get('/api/v1')
async def root():
    return {"message":'Best api in the world'}

from user.routes import *
from bot_api.routes import *

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port = 8080)