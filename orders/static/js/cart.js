document.addEventListener('DOMContentLoaded', (event) => {

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
                },
                error : function(xhr,errmsg,err) {
                    console.log("something went wrong...")
                }
            });
        }
    )
})

