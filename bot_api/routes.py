from functools import wraps
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from app import app
from bot_api.models import Bot
from decorators import login_required, access_level
import pdb


@app.get('/status/')
async def status(request:Request):
    # pdb.set_trace()
    ping = await Bot().ping()
    # return ping
    print(ping)
    return jsonable_encoder(ping)