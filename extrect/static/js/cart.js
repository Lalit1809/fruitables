$(document).ready(function() {
    // Attach click event handler to both buttons
    $('#minus_icon, #plus_icon').click(function() {
        var button = $(this);
        var action = $(button).attr('action'); 
        var product_id = button.data('product-id'); 
        console.log('Action:', action);
        console.log('Product ID:', product_id);

        var formData = new FormData()
        formData.append('product_id',product_id);
        formData.append('action',action);
        // console.log(formData,'this is the formData');
        
        $.ajax({
            url:'/update_cart/',
            type:'POST',
            data:formData,
            processData: false,
            contentType: false,      
            success:function(response){
                if (response.success) {
                    // update quantity input field
                    button.closest('.quantity').find('input').val(response.quantity);

                    // update item price
                    button.closest('tr').find('td:nth-child(5) p').text('₹' + response.item_price);

                    // update total cart price
                    $('.py-4 .pe-4').text('₹' + response.total_price);
                }
                console.log('card update',response)
            },
            error:function(xhr, status, error){
                console.log('ERROR',error)
            }

        });   
    });
});