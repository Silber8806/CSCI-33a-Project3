document.addEventListener('DOMContentLoaded', (event) => {

    let order_form_inputs = Array.prototype.slice.apply(document.querySelectorAll("input"));

    order_form_inputs.forEach((input_form) => {
        input_form.onclick = function(event){
            console.log("I Clicked..");
        }
    });
});