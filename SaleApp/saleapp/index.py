from flask import Flask, render_template,request
import dao

app = Flask(__name__)


@app.route('/')
def index():
    q = request.args.get('q')

    cate_id = request.args.get('catergory_id')
    categories = dao.load_catergories()
    products = dao.load_products(cate_id)
    return render_template('index.html', categories=categories, products=products)


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
