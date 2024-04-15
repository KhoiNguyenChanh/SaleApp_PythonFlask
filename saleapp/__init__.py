import cloudinary
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# Nếu trong mật khẩu MySQL có chưa ký tự đặc biệt, ta có thể làm như sau:
from urllib.parse import quote
# tao dang nhap dang ky
from flask_login import LoginManager
# babel lỗi :)))))
# muốn đa ngôn ngữ -> cho người dùng chọn ngôn ngữ họ muốn ->flask babellex
from flask_babel import Babel  # Import Flask-Babel
# from flask_babelex import Babel
# from flask.ext.babelex import Babel
app = Flask(__name__)  # ten app thuong la ten module -> dung bien toan cuc

# them 1 cate mơi -> The session is unavailable because no secret key was set.  Set the secret_key on the application to something unique and secret.
# ->tao secret key
app.secret_key = '!@$%^&*()'  # shift 1234567890

# cau hinh ket noi database
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:%s@localhost/saledbpy' % quote('Admin@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 6
# keycart
app.config["cart"] = 'cart'

# tu dau den cuoi chi co 1 doi tuong
db = SQLAlchemy(app)
login = LoginManager(app)

# cloudinaty
cloudinary.config(cloud_name='dbqaequqv',
                  api_key='741317942552615',
                  api_secret='L05czfd2tdEhRvbUy29A1vF8BZ4')
# #babel
babel = Babel(app=app)
# @babel.localeselector
def get_locale():
#     #  Put your logic here. Application can store locale in
#     #  user profile, cookie, session, etc.
    return 'en', 'vi'
app.jinja_env.globals['get_locale'] = get_locale
