from saleapp import db, app
from enum import Enum as RoleEnum
from sqlalchemy import Column, String, Float, Integer, ForeignKey, Enum
# tao doi tuong?
from sqlalchemy.orm import relationship
from flask_login import UserMixin


# User role
class UserRole(RoleEnum):
    USER = 1,
    ADMIN = 2,


# tao user trong model cho viec logi
class User(db.Model, UserMixin):
    # phai co primary key
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(100))
    avatar = Column(String(100))
    username = Column(String(50), unique=True)
    password = Column(String(50))
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    def __str__(self):
        return self.name


# 1 sanpham có 1 cate, 1 cate co nhieu san pham
class Category(db.Model):  # muon tao db thanh cong phai ke thua db.Model
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    # thietlap relationship với bảng product ben duoi :1
    # co 2 thuoc tinh quan trong thuoc relationshop
    # backref tư gan doi tuong 'doi tuong' vao cai dai dien cua no trong product
    # lazy -> khi lay 1 cate ra thi chua truy van cai bien products (ngay ben duoi)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Product(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    price = Column(Float, default=0)
    image = Column(String(100),
                   default='https://res.cloudinary.com/dbqaequqv/image/upload/v1710207638/samples/logo.png')
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)

    # category_id là khoa ngoai tham chieu toi Category.id, can phai chi ro ra ntn, giá trị bắt buộc (nullable=False-> ko dc để trống)

    # tao ghi de khoa ngoai
    def __str__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # c1 = Category(name='Mobile')
        # c2 = Category(name='Tablet')
        # c3 = Category(name='Laptop')
        # db.session.add_all([c1,c2,c3])
        # db.session.commit()
        #
        # import json
        # with open('data/products.json', encoding='utf-8') as f:
        #     # chua tra ra du lieu lien -> (l) index.py
        #     products = json.load(f)
        #     # ep toan bo trong database vao
        #     for p in products: # hien h p la cuc data json producst
        #         # lay name, price, image
        #         prod = Product(**p) # **p tuong duong voi name=p['name'], price=p['price'],...
        #         # sau do dua vao session de add
        #         db.session.add(prod)
        #
        # db.session.commit()

        # password bi bam
        import hashlib

        u = User(name='admin',
                 username='admin',
                 avatar='https://res.cloudinary.com/dbqaequqv/image/upload/v1710207638/samples/logo.png',
                 password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                 user_role=UserRole.ADMIN)
        db.session.add(u)
        db.session.commit()
# run lan 1: loi image dai qua la sao :1?
