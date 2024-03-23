from sqlalchemy import Column, String, Float, Integer, ForeignKey
from saleapp import db, app
from sqlalchemy.orm import relationship


class Category(db.Model):  # hóa entity model
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    products = relationship('Product', backref='category', lazy=True)  # tranhs truy vaans product

    def __str__(self):
        return self.name


class Product(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    price = Column(Float, default=0)
    image = Column(String(100), default="https://res.cloudinary.com/dxxwcby8l/image/upload/v1679731974/jlad6jqdc69cjrh9zggq.jpg")
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # c1 = Category(name="Mobile")
        # c2 = Category(name="Tablet")
        # db.session.add_all([c1, c2])
        # db.session.commit()
        import json
        with open('data/products.json', encoding='utf-8') as f:
            products = json.load(f)
            for p in products:
                prod = Product(**p)  # better
               # prod = Product(name=p['name'], price=p['price']) #alternate, worse
                db.session.add(prod)

        db.session.commit()
