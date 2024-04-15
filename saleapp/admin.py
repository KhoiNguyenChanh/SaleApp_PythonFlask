from flask_admin import Admin, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView
from saleapp.models import Category, Product, UserRole
from saleapp import app, db
from flask_login import logout_user, current_user
from flask import redirect


# tao class rieng cho cai def is authenticated :1?
# authenticated view ke thua model view r nen ko can goi o cac view khac neu no ke thua authenticaetd viw
class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


# tao class xong thi chi can goi them trong cai () la dc :)
# va phai dat cai authen trc moi thu con lai :1
# customize de co the them Product
class MyProductView(AuthenticatedView):
    # them cac cot co ten id, name, cate_id, them price
    column_list = ['id', 'name', 'category_id', 'price']
    # them 1 thanh search với place holder là id, name
    column_searchable_list = ['id', 'name']
    # them filter cho id, name, price, filter co eq, >= <=,....
    column_filters = ['id', 'name', 'price']
    # can_export no se them 1 cai export de export ra file csv
    can_export = True
    # edit, cac ten thuoc phan [[]] xuat hien mau xanh bien, nhap vao co the edit tai cho
    column_editable_list = ['name', 'price']
    # column label de doi ten cac cot
    column_labels = {
        'name': 'Tên sản phẩm',
        'category_id': 'Danh mục',
        'price': 'Giá tiền',
        'id': 'Mã sản phẩm (id)'

    }

    # de chi khi dang nhap thi moi hien ra các trang


# tao khoa ngoai trong phan create product -> tim catergory
class MyCategoryView(AuthenticatedView):
    column_list = ['id', 'name', 'products']
    # muon tao cac cot nhu tren productview thi cu copy o tren xuong ma dung :1?


class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')


# logout
class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


admin = Admin(app, name='Ecommerce Website', template_mode='bootstrap4')
admin.add_view(MyCategoryView(Category, db.session, name='Danh mục'))
admin.add_view(MyProductView(Product, db.session, name='Sản phẩm'))
admin.add_view(StatsView(name='Thống kê'))
# name doi ten hien thi
admin.add_view(LogoutView(name='Đăng xuất'))
# de trong admin thi trang admin tu hien ra tren thanh navbar :0
