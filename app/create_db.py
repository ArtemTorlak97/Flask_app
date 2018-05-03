#!/usr/bin/python3.5
import models
from app import db
db.create_all()
from models import Post
p = Post(title = 'First post', body = 'First post body')
db.session.add(p)
db.session.commit()
p1 = Post(title = 'Second post', body = 'Second post body')
db.session.add(p1)
db.session.commit()
p2 = Post(title = 'Third post! 3-test', body = 'Third post body')
db.session.add(p2)
db.session.commit()
