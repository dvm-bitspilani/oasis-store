var cart_id="";
window.onload = function(){
  jQuery(function($){
    // get cart from cache
    $.ajax({
      type:'GET',
      url:'../../getcart/',
      success:function(response){
        dataArr=response['items'];
        cart_id=response['cart_id'];
        console.log(dataArr);
        dataArr.map(function(data){

        var newItem = $('.default__item').clone();
        newItem.show();
        newItem.removeClass('default__item');
        newItem.find('.shopping-cart__item__info__title').html(data.name);
        newItem.find('.shopping-cart__item__image img').attr('src',data.img);
        newItem.find('.shopping-cart__item__info__price').html(parseInt(data.price)*parseInt(data.quantity));
        newItem.find('.shopping-cart__item__info__size span').html(data.size);
        newItem.find('.shopping-cart__item__info__color span').html(data.color);
        newItem.find('.shopping-cart__item__info__qty span').html(data.quantity);

        $('#cart-list').append(newItem);
      });
        // console.log('hi');
        updateCart();

      }
    })
  });
}

jQuery(function($){
  var loc=location.href;

  var data={};
console.log($('.product-name').attr('data-id'));
$('#add-cart').click(function(){
  data={
    'itemID': $('.product-name').attr('data-id'),
    'name': $('.product-name').html(),
    'price': $('.product-price').html(),
    'quantity': $('.product-quantity').val(),
    'size': $('.product-size').val(),
    'color': $('.product-color').val(),
    'img': $('.product-img').attr('src')
  }

  $.ajax({
    type:'POST',
    url:'../../buy/',
    data:data,
    success:function(response){
      var respData = response.data;
      console.log(response,respData);
      if(response.status='True'){
        alert(response.message)
        // add new item
        var newItem = $('.default__item').clone();
        newItem.show();
        newItem.removeClass('default__item');
        newItem.find('.shopping-cart__item__info__title').html(data.name);
        newItem.find('.shopping-cart__item__image img').attr('src',data.img);
        newItem.find('.shopping-cart__item__info__price').html(parseInt(data.price)*parseInt(data.quantity));
        newItem.find('.shopping-cart__item__info__size span').html(data.size);
        newItem.find('.shopping-cart__item__info__color span').html(data.color);
        newItem.find('.shopping-cart__item__info__qty span').html(data.quantity);

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
  jQuery(function($){
  item_id=$('.product-name').attr('data-id');
  var data={
    cartid:cart_id+item_id,
  }
  $.ajax({
    type:'POST',
    url:'../../items/removeitem/',
    data:data,
    success:function(response){
        alert(response.message);
        $(ele).closest('.shopping-cart__item').remove();
        updateCart();
    }
  });
});
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
