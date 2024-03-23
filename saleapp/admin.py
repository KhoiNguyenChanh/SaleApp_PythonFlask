from flask_admin import Admin
from saleapp import app, db
from flask_admin.contrib.sqla import ModelView
from saleapp.models import Category, Product


class MyProductView(ModelView):
    column_list = ["id", "name", "category_id"]


class MyCategoryView(ModelView):
    column_list = ["id", "name", "products"]


admin = Admin(app, name="Ecommerce", template_mode="bootstrap4")
admin.add_view(MyCategoryView(Category, db.session))
admin.add_view(MyProductView(Product, db.session))
