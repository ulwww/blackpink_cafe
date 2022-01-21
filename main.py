from flask import Flask
import socket

from routes import add_routes
from database import DataBase


database = DataBase()
app = Flask(__name__)
add_routes(app, database)
app.run(host=socket.gethostbyname(socket.gethostname()), port=80)
