from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Security key. import secrets, secrets.token_hex(16)
app.config['SECRET_KEY'] = '0480350659cd7743a0164e35e2ba0abb'
app.config['DEBUG'] = False
app.config['THREADS_PER_PAGE'] = 4
app.config['CSRF_ENABLED'] = True

from tool import routes
