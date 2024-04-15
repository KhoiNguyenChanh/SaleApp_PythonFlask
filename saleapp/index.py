import math

# session la lam viec voi server, phai vao init cau hinh secret key, neu cau hinh session loi thi co nghia chua lam ben init
from flask import render_template, request, redirect, session, jsonify
# cac doi tuong tu client sver deu do request tu client goi len -> import request
# (l) import dao
import dao
import utils
from flask_login import login_user, current_user, logout_user
# sau khi move, no tu import qua
from saleapp import app, admin, login
import cloudinary.uploader
#can dung decorator nen import
from decorators import loggedin

# chay tu index, phải import admin, neu ko no ko biet  admin

# ten cau hinh dua vao init, init chưa toan bo cau hinh
# khi move thi dung boi den

# chay trnag chu?
# render_template chay response ve html
# !!!Gan @app.route
@app.route('/')
def index():
    # quy luat render_template se tim folder templates de lay index.html tra ve r render len server
    # truyen du lieu dua ra ngoai link, nhap nhu ben duoi (tao1bien name, sau index.html nhap name= bien name, sau do
    # qua index.html de thuc hien dua ra ngoai link , (l): dau hieu cho doan code hien
    # name = "Chanh Khoi"
    # return render_template('index.html', name=name)

    # quy uoc java ấy đường dẫn
    # lay dc tat cac cac ky tu, nhung bi buoc phai dung chu cai trong ten
    q = request.args.get('q')
    cate_id = request.args.get('category_id')
    # them page vao
    page = request.args.get("page")

    # (l), sau do sang index.html de xuat data
    # categories = dao.load_categories()
    # dat ben trong product q và cateid ->(l) qua dao
    products = dao.load_products(q=q, cate_id=cate_id, page=page)
    # print(categories)
    return render_template('index.html', products=products,
                           pages=math.ceil(dao.count_product() / app.config['PAGE_SIZE']))
    # pages=dao.count_product()/app.config['PAGE_SIZE'] NHU THE NAY SE RA LE, 1.1 = PAGE 2


# define đường dẫn khác /, hướng dẫn truyền bằng pass param
# rangf buoc id là so nguyen int:id
@app.route('/products/<int:id>')
def details(id):
    product = dao.get_product_by_id(product_id=id)
    return render_template('product-details.html', product=product)


# gắn cái context processor vào, mọi response sẽ găns cái common att vào
@app.context_processor
def common_attributes():
    return {
        'categories': dao.load_categories()

    }


# có 3 loại response, loại html vừa làm, loại redirect, và loại json
@app.route('/login', methods=['get', 'post'])
@loggedin
def login_my_user():
    # kiem tra neu da login thi ko hien man hinh login ra nua
    # import current user trong flasklogin
    # 1.Da dang nhap xong nhung khi vao register van dc -> ko on
    # 2.thuc te cai kiem tra ng dung ko nen nam trong logic login
    if current_user.is_authenticated:
        return redirect('/')
    err_msg = ''
    if request.method.__eq__('POST'):
        # print(request.form)
        # vd redirect
        username = request.form.get('username')
        password = request.form.get('password')
        # redirect ve trang chu dang nhap -> ghi nhan trang thai dang nhap vao session
        user = dao.auth_user(username=username, password=password)
        # login that
        if user:  # user ! null
            login_user(user)
            return redirect('/')
        else:
            err_msg = 'Tài khoản hoặc mật khẩu không đúng!'
        # #login gia
        # if username.__eq__('admin') and password.__eq__('123'):
        #     # chuyn ve trang chu, nho import redirect
        #     return redirect('/')

    return render_template('layout/login.html', err_msg=err_msg)


@app.route('/logout', methods=['get'])
def logout_my_user():
    logout_user()
    return redirect('/login')


@app.route('/admin-login', methods=['post'])
def process_admin_login():
    # request.form(name='' o ben index.html)
    username = request.form.get('username')
    password = request.form.get('password')
    u = dao.auth_user(username=username, password=password)
    # neu u ton tai
    if u:
        login_user(user=u)

    # fail hay succ thi cung ve trang quan tri
    return redirect('/admin')


@app.route('/register', methods=['get', 'post'])
@loggedin # chu yeu ngan ko cho vao trong register/login sau khi da dang nhap thanh cong
def register_user():
    err_msg = None
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if password.__eq__(confirm):
            avatar_path = None
            # 'avatar' là trường khai bao biên name bên register
            avatar = request.files.get('avatar')
            if avatar:
                # import cloudinary.uploader
                res = cloudinary.uploader.upload(avatar)
                avatar_path = res['secure_url']

            # thu try catch neu co vande
            dao.add_user(
                name=request.form.get('name'),
                username=request.form.get('username'),
                password=password,
                avatar=avatar_path)

            return redirect('/login')
        else:
            err_msg = 'Mật khẩu không đúng'
    return render_template('/layout/register.html', err_msg=err_msg)


# cach them duong link moi
# man hinh khác
# @app.route('/register')
# def register_user():
#     return render_template('register.html')


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


# viet api
@app.route('/api/carts', methods=['post'])
def add_to_cart():
    """
      "cart":{
          "1":{
              "id": ""
              "name": ""
              "price": ""
              "quantity": 2
          },
          "2":{
              "id": ""
              "name": ""
              "price": ""
              "quantity": 2
          },
      }

    :return:
    """
    # 'cart' la key tu cau hinh, neu sua thi vao innit cau hinh luon
    cart = session.get('cart')
    if not cart:  # neu gio rong, hoa ra day la cach thong bao not :)
        cart = {}

    id = str(request.json.get('id'))
    if id in cart:
        # da co trong gio
        cart[id]["quantity"] += 1

    else:  # chua co rong gio
        cart[id] = {
            "id": id,
            "name": request.json.get("name"),
            "price": request.json.get("price"),
            "quantity": 1  # mac dinh la 1 khi lan dau bam vao them gio hang
        }

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))

# chay sver
if __name__ == '__main__':
    with app.app_context():  # chay trong ngu canh cua ung dung
        app.run(debug=True)

# Comment abt running app down here
# !!!chay lan 1,url not found-> do chua gan @app.route('/') de dinh tuyen, cai nay nam tren def index(), dung de chay sver
# !!!chay lan 2, sau khi gan app.route thi da hien len trang web
# ??? de ket noi csdl that -> dung flask sqlalchemy
