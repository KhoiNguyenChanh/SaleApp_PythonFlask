# khac voi dao di truy van database
# utils chi la cac ham tien ich cho toan bo chuong trinh

# tao thong ke
def count_cart(cart):
    total_amount, total_quantity = 0, 0
    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_amount += c['quantity'] * c['price']
    return {
        "total_amount": total_amount,
        "total_quantity": total_quantity,

    }
