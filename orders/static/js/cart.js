document.addEventListener('DOMContentLoaded', (event) => {

    function format_currency(currency){
        return parseFloat(Math.round(currency * 100) / 100).toFixed(2);
    }

    function calculate_total_basket(){
        let current_total = 0.00;
        let cart_items = Array.prototype.slice.apply(document.getElementsByClassName('add-to-cart-item'))

        if (cart_items.length == 0) {
            checkout_btn.setCustomValidity("No Items in Cart!");
            no_items.style.display = "block";
        } else {
            checkout_btn.setCustomValidity("");
            no_items.style.display = "none";
        }

        cart_items.forEach((cart_item) =>
            current_total += parseFloat(cart_item.dataset.price)
        )

        document.getElementById("total-checkout").value = format_currency(current_total);
    }

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

    Array.prototype.slice.apply(document.getElementsByClassName("kill-cart-line")).forEach((cancel_button) =>
        cancel_button.onclick = function(event){
            let item_to_delete = this.dataset.id;
            let jsonData = { item: item_to_delete };
            let cart = this.parentNode.parentNode.parentNode;
            let cart_line_item = this.parentNode.parentNode;

            $.ajax({
                "type": "DELETE",
                "dataType": "json",
                "url": "/removefromcart/",
                "data": jsonData,
                "success": function(result) {
                   cart.remove(cart_line_item);
                   calculate_total_basket();
                },
                error : function(xhr,errmsg,err) {
                    console.log("something went wrong...")
                }
            });
        }
    )

    var checkout_btn = document.getElementById("checkout-btn");
    var no_items = document.getElementById("no-items")

    calculate_total_basket()
})

