from functools import wraps
from fastapi import FastAPI, Request
from app import app
from bot_api.models import Bot
from decorators import login_required, access_level
import pdb


@app.route('/status/', methods = ['GET'])
async def status(request:Request):
    # pdb.set_trace()
    ping = await Bot().ping()
    # return ping
    return ping