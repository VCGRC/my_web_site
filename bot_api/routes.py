from functools import wraps
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from app import app
from bot_api.models import Bot
from decorators import login_required, access_level
import pdb


@app.get('/api/v1/bot/status')
async def status(request:Request):
    ping = await Bot().ping()
    return jsonable_encoder(ping)