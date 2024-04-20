
$(document).ready(function(){
    $(".add-to-cart-btn").on("click", function (){
    let this_val = $(this)
    let index = this_val.attr("data-index")

    let quantity = $("#product-quantity-"+index).val()
    let product_image = $(".product-image-"+index).val()
    
    let product_pid = $(".product-pid-"+index).val()
    let product_title = $(".product-title-"+index).val()
    
    let product_id = $(".product-id-"+index).val()
    let product_price = $(".current-product-price-"+index).text()
    

    console.log("Qte: ",quantity);
    console.log("Designation: ",product_title);
    console.log("Prix: ", product_price);
    console.log("Image: ",product_image);
    console.log("Id: ",product_id);
    console.log("PId: ",product_pid);
    console.log("Current Element: ",this_val);
    console.log("Index: ", index);

    $.ajax({
        url : '/add-to-cart',
        data : {
            'id': product_id,
            'pid': product_pid,
            'image': product_image,
            'qty': quantity,
            'title': product_title,
            'price': product_price,
        },
        dataType: 'json',
        beforeSend: function(){
            console.log("Adding to cart...");
        },
        success: function(response){
            this_val.html("✔")
            console.log("Added Product to cart");
            $(".cart-items-count").text(response.totalcartitems)
        }
    })
})

$(".delete-product").on("click", function(){
    let product_id = $(this).attr("data-product")
    let this_val = $(this)

    console.log("Product Id:", product_id)

    $.ajax({
        url:"/delete-from-cart",
        data: {
            "id":product_id
        },
        dataType: "json",
        beforeSend: function(){
            this_val.hide()
        },
        success: function(response){
            this_val.show()
            $(".cart-items-count").text(response.totalcartitems)
            $("#cart-list").html(response.data)
        }
    })
})

$(".update-product").on("click", function(){
    let product_id = $(this).attr("data-product")
    let this_val = $(this)
    let product_quantity = $(".product-qty-"+product_id).val()

    console.log("Product Id:", product_id);
    console.log("Product Qty:", product_quantity);


    $.ajax({
        url:"/update-cart",
        data: {
            "id":product_id,
            "qty":product_quantity,
        },
        dataType: "json",
        beforeSend: function(){
            this_val.hide()
        },
        success: function(response){
            this_val.show()
            $(".cart-items-count").text(response.totalcartitems)
            $("#cart-list").html(response.data)
        }
    })
})
})
