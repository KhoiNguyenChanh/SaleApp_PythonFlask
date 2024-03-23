from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "!@#$%^&*()(*&^%$#@!"  # 1-9-1
#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/saledb?charset=utf8mb4"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/saledb?charset=utf8mb4' % quote('Admin@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 2 #de dai thoi, cho ra phantrang
db = SQLAlchemy(app)