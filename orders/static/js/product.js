document.addEventListener('DOMContentLoaded', (event) => {

    let quantity_box = document.getElementById('quantity');
    let purchase_amount = document.getElementById('purchase-total');
    let base_price = document.getElementById('product_id').dataset.price;
    let order_form_inputs = Array.prototype.slice.apply(document.querySelectorAll("input"));

    order_form_inputs.forEach((input_form) => {
        input_form.onchange = function(event){
            console.log("I Clicked..");
        }
    });

    document.getElementById('big-plus').onclick = function(event){
        if (quantity_box === "") {
            quantity_box.value = 1;
        } else {
            quantity_box.value += 1;
        }
    }

    document.getElementById('big-plus').onclick = function(event){
        let modify_val = parseInt(quantity_box.value);
        modify_val += 1;
        quantity_box.value = modify_val;
    }

    document.getElementById('big-minus').onclick = function(event){
        let modify_val = parseInt(quantity_box.value);
        modify_val -= 1;
        if (modify_val >= 1) {
            quantity_box.value = modify_val;
        }
    }
});