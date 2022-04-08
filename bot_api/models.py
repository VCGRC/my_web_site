from flask import Flask, jsonify, redirect, request, session
from passlib.hash import pbkdf2_sha256
import uuid
from app import cluster, app
from nextcord.ext import ipc


user_collection = cluster.web.status
ipc_client = ipc.Client(secret_key=app.secret_key)

class Bot:

    async def ping(self) -> float:
        ping = await ipc_client.request('get_ping')

        return str(ping) 
