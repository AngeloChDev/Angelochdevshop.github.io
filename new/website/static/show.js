function show_cart() {
    var cart = document.getElementById("cart_div");
    
    if (cart.style.display === "none") {
        cart.style.display = "block";
    } else {
        cart.style.display = "none";
    }};

function show_product_list(){
    var product_list = document.getElementById("product_list_div");
    
    if (product_list.style.display === "none") {
        product_list.style.display = "block";
    } else {
        product_list.style.display = "none";
    }};


function myShow() {
    var x = document.getElementById("in_data_row");
    var y = document.getElementById("email_btn");
    if (x.style.display === "none") {
        x.style.display = "block";
        y.style.display = "block";
    } else {
        x.style.display = "none";
        y.style.display = "none";
    }};

function myEmail() {
    var y = document.getElementById("email_d");
    var x = document.getElementById("email_btn");
    var p = document.getElementById("pay_btn");

    if (y.style.display === "none") {
        y.style.display = "block";
        x.style.display = "none";
        p.style.display = "block";
    } else {
        y.style.display = "none";
    }};



function myPay() {
    var y = document.getElementById("pay_data");
    var x = document.getElementById("pay_btn");
    var s = document.getElementById("submit");

    if (y.style.display === "none") {
        y.style.display = "block";     
        x.style.display = "none"; 
        s.style.display = "block"; 
    } else {
        y.style.display = "none";
    }
}