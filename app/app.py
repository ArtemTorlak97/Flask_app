#!/usr/bin/python3.5
from flask import Flask
from config import Configuration
#import value posts (object of class blueprint)
from posts.blueprint import posts

app = Flask(__name__) 
app.config.from_object(Configuration)
app.register_blueprint(posts, url_prefix='/blog')