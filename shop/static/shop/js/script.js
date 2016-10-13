window.onload = function(){
  jQuery(function($){
    // get cart from cache
    $.ajax({

    })
  });
}

jQuery(function($){
  var loc=location.href;

  var data={
    'itemID': loc.substring(loc.indexOf('product/')+8,loc.length-1),
    'name': $('.product-info__title h2').html(),
    'price': $('.price-box__new').html(),
    'quantity': $('.select-quantity').val(),
    'size': $('.select-size').val(),
    'color': $('.select-color').val(),
  }


$('#add-cart').click(function(){

  $.ajax({
    type:'POST',
    url:'../../buy',
    data:data,
    success:function(response){
      var respData = response.data;
      console.log(response,respData);
      if(response.status='True'){
        alert(response.message)
        var newItem = $('.default__item').clone();
        newItem.show();
        newItem.removeClass('default__item');
        newItem.find('.shopping-cart__item__info__title').html(respData.name);
        newItem.find('.shopping-cart__item__info__price').html(respData.price);
        newItem.find('.shopping-cart__item__info__size span').html(respData.size);
        newItem.find('.shopping-cart__item__info__color span').html(respData.color);
        newItem.find('.shopping-cart__item__info__qty span').html(respData.qty);

        $('#cart-list').append(newItem);
        // console.log('hi');
        updateCart();

      }

    }
  })

});

$('.icon-clear').click(function(){

})

});

function delete_item(ele){
  console.log(ele);
  jQuery(ele).closest('.shopping-cart__item').remove();
  updateCart();
}

function updateCart(){
  var sum=0;
  jQuery(function($){

  $('#cart-list').children().map(function(i,e){
    amt=parseInt($(e).find('.shopping-cart__item__info__price').html());
    sum=sum+amt;
  });
  $('.shopping-cart__total').html(sum);
  $('.cart-items-no').html($('#cart-list').children().length-1);
  });
}
