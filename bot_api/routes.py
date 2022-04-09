from functools import wraps
from quart import Quart, redirect, render_template, session, request, url_for, current_app
from app import app
from bot_api.models import Bot
from decorators import login_required, access_level
import pdb


@app.route('/status/', methods = ['GET'])
@access_level
async def status():
    # pdb.set_trace()
    ping = await Bot().ping()
    # return ping
    return await render_template('status.html', ping = ping)