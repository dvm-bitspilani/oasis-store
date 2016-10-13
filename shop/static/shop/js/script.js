window.onload = function(){
  jQuery(function($){
    // get cart from cache
    // $.ajax({
    //   type:'GET',
    //   url:'../../buy/',
    //
    // })
  });
}

jQuery(function($){
  var loc=location.href;

  var data={};

$('#add-cart').click(function(){
  data={
    'itemID': loc.substring(loc.indexOf('product/')+8,loc.length-1),
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
