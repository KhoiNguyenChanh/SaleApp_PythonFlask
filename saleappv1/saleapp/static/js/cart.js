//function addtoCart
function addToCart(id, name, price) {
    fetch("/api/carts", {
       method: "post",
       body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
       }),
       headers: {
            "Content-Type": "application/json"
       }
    }).then(res => res.json()).then(data => {
        let d = document.getElementsByClassName("cart-counter");
        for (let e of d)
            e.innerText = data.total_quantity;
    })
}
//funcion updatecart,
//them onblur goi updateCart({{c,id}}) ben kia se lam thay doi so luong hang dat khi nhap chuot ra cho khac
function updateCart(productId, obj){
    fetch (`/api/cart/${productId}`, {
        method:"put",
        body: JSON.stringify({
            "quantity": parseInt(obj.value)
        }),
       headers: {
            "Content-Type": "application/json"
       }
    }).then(res => res.json()).then(data => {
            //for so luong - quantity
            let d = document.getElementsByClassName("cart-counter");
            for (let e of d)
                e.innerText = data.total_quantity;
            //for tong tien - amount
            let d2 = document.getElementsByClassName("cart-amount");
            for (let e of d2)
                e.innerText = data.total_amount.toLocaleString("en");
    });
}

//function del cart
function deleteCart(productId){
    if(confirm("Bạn muốn xóa sản phẩm khỏi giỏ hàng?") === true) {
        fetch (`/api/cart/${productId}`, {
            method:"delete"
        }).then(res => res.json()).then(data => {
                //for so luong - quantity
                let d = document.getElementsByClassName("cart-counter");
                for (let e of d)
                    e.innerText = data.total_quantity;
                //for tong tien - amount
                let d2 = document.getElementsByClassName("cart-amount");
                for (let e of d2)
                    e.innerText = data.total_amount.toLocaleString("en");
                //get 1 Element by ID
                //ben cart.html, <tr id=" product{{ c.id}} ", ben day dò theo 1.product 2.id để xóa, có thể custom lại
                let e = document.getElementById(`product${productId}`);
                //let e = document.getElementById(`${productId}`); -test custom
                e.style.display = 'none';
        });

    }//ket thuc if
}//ket thuc function


