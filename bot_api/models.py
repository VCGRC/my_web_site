import pdb
from passlib.hash import pbkdf2_sha256
import uuid
from app import cluster, app
from nextcord.ext import ipc
import pdb
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


user_collection = cluster.web.status
ipc_client = ipc.Client(secret_key=os.environ.get('SECRET_KEY'))

class Bot:

    async def ping(self) -> dict:
        # pdb.set_trace()
        ping = await ipc_client.request('get_ping')

        return ping
