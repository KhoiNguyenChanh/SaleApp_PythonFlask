import json


def load_catergories():
    with open("data/categories.json", encoding="utf-8") as f:
        return json.load(f)


def load_products(q=None, cate_id=None):
    with open("data/product.json", encoding="utf-8") as f:
        return json.load(f)

    if q:
        products = [p for p in producst if p ["name"].find(q) >= 0]

    if cate_id:
        products = [p for p in products if (p["category_id"].__eq__(int(cate_id)))]

    return products


if __name__ == ("__main__"):
    print(load_catergories())
    print(load_products())