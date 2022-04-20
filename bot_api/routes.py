from functools import wraps
from fastapi import FastAPI
from app import app
from bot_api.models import Bot
from decorators import login_required, access_level
import pdb

@access_level(level=5)
@app.route('/status/', methods = ['GET'])
async def status():
    # pdb.set_trace()
    ping = await Bot().ping()
    # return ping
    return ping