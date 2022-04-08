from functools import wraps
from flask import Flask, redirect, render_template, session, request, url_for
from app import app
from bot_api.models import Bot
from decorators import login_required, access_level


@app.route('/status/', methods = ['GET'])
async def status():
    ping = await Bot().ping()
    return render_template('status.html', ping = ping)