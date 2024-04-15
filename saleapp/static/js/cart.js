function addToCart(id, name, price){
    fetch("/api/carts",{
    method: "post",
    body: JSON.stringify({
            //phai la chuoi chu ko phai doi tuong
            "id": id,
            "name": name,
            "price": price
        }),
        headers:{
             "Content-Type": "application/json"
        }

    }).then(res => res.json()).then(data => {
        console.info(data)
        //cart-counter nam trong class gio hang ben headerhtml
        let d = document.getElementsByClassName("cart-counter");
        for (let e of d)
            e.innerText = data.total_quantity;
    })
}