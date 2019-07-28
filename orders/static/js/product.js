document.addEventListener('DOMContentLoaded', (event) => {

    function format_currency(currency){
        return parseFloat(Math.round(currency * 100) / 100).toFixed(2);
    }

    function calculate_price() {
        let options_priced = 0;
        product_options.forEach((option) => {
            if (option.checked && option.dataset.price != 0){
                options_priced += parseFloat(option.dataset.price);
            }
        });

        let per_unit_price = format_currency( parseFloat(base_price) + options_priced)
        let current_price =  format_currency(quantity_box.value * per_unit_price);
        purchase_amount.innerHTML = current_price;
        per_unit_price_input.value = per_unit_price;
        order_total_amount.value = current_price;
    }

    function is_valid_toppings() {
        let checked_toppings = 0;
        toppings.forEach((topping) => {
            if(topping.checked){
                checked_toppings += 1;
            }
        });

        if (min_value > checked_toppings || max_value < checked_toppings) {
            if (min_value == max_value) {
                order_btn.setCustomValidity(`${min_value} toppings allowed`);
            } else {
                order_btn.setCustomValidity(`${min_value}-${max_value} toppings allowed`);
            }
            return 0;
        }
        order_btn.setCustomValidity("");
        return 0;
    };

    function set_up_event_handlers() {
        toppings.forEach((topping) => {
            topping.onclick = function(event){
                is_valid_toppings();
                return true
            }
        });

        order_form_inputs.forEach((input_form) => {
            input_form.onchange = function(event){
                calculate_price();
            }
        });

        document.getElementById('big-plus').onclick = function(event){
            let modify_val = parseInt(quantity_box.value);
            modify_val += 1;
            quantity_box.value = modify_val;
            calculate_price();
        }

        document.getElementById('big-minus').onclick = function(event){
            let modify_val = parseInt(quantity_box.value);
            modify_val -= 1;
            if (modify_val >= 1) {
                quantity_box.value = modify_val;
                calculate_price();
            }
        }
    };

    let quantity_box = document.getElementById('quantity');
    let purchase_amount = document.getElementById('purchase-total');
    let order_total_amount = document.getElementById('order-total');
    let per_unit_price_input = document.getElementById('per-unit-price');
    let base_price = document.getElementById('product_id').dataset.price;
    let order_form_inputs = Array.prototype.slice.apply(document.querySelectorAll("input"));
    let product_options = Array.prototype.slice.apply(document.getElementsByClassName("option-inputs"));
    let toppings = Array.prototype.slice.apply(document.getElementsByClassName("toppings"));
    let order_btn = document.getElementById('order-btn');
    let min_value = parseInt(document.getElementById('option-num-min').value);
    let max_value = parseInt(document.getElementById('option-num-max').value);

    is_valid_toppings();

    purchase_amount.innerHTML = base_price;


    set_up_event_handlers()
});