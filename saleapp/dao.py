# quy uoc, tu nay ve sau, moi khi doc/truy xuat data se dung "dao"
# import json -> ko dùng nữa

from saleapp import app, db
from saleapp.models import Category, Product, User
import hashlib


# !truy van don gian!
# loc categories
def load_categories():
    return Category.query.all()
    # with open('data/categories.json', encoding='utf-8') as f:
    #     return json.load(f)


# dem so luong spham -> so page
def count_product():
    return Product.query.count()


# loc du lieu product
# 2 prop dc gui, mac dinh ko gui thi None
# phan trang, them page vao loadproduct, phan trang thu cong -> can cau hinh page size -> vo innit
def load_products(q=None, cate_id=None, page=None):
    query = Product.query

    if q:
        # string thì contains, số thì eq
        query = query.filter(Product.name.contains(q))
    if cate_id:
        query = query.filter(Product.category_id.__eq__(cate_id))
    if page:
        page_size = app.config["PAGE_SIZE"]
        start = (int(page) - 1) * page_size
        query = query.slice(start, start + page_size)

    return query.all()
    # ben tren la lay data thật
    # ben duoi lay data tu tao (gia)
    # with open('data/products.json', encoding='utf-8') as f:
    #     #chua tra ra du lieu lien -> (l) index.py
    #     products = json.load(f)
    #     # tim cau lenh: ''.
    #     #find dung de tim co chua keyword muon tim-> dung find
    #     if q: #if q = default là None
    #         products = [p for p in products if p['name'].find(q) >= 0]
    #
    #     if cate_id:
    #         products = [p for p in products if p['category_id'].__eq__(int(cate_id))]
    #
    #     return products


def get_product_by_id(product_id):
    return Product.query.get(product_id)
    # with open('data/products.json', encoding='utf-8') as f:
    #     products = json.load(f)
    #     for p in products:
    #         if p['id'] == product_id: #id ng ta truyền vào
    #             return p


def get_user_by_id(id):
    return User.query.get(id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def add_user(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name, username=username, password=password, avatar=avatar)
    db.session.add(u)
    db.session.commit()


if __name__ == '__main__':
    print(load_categories())

# di qua index.py de thuc hien lay data + xuat? ki hieu (l)
