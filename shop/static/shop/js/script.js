jQuery(function($){

$('#add-cart').click(function(){
  var newItem = $('.default__item').clone();
  newItem.show();
  newItem.removeClass('default__item');
  newItem.find('.shopping-cart__item__info__title').html($('.product-info__title').html());
  newItem.find('.shopping-cart__item__info__price').html($('.price-box__new').html());
  newItem.find('.shopping-cart__item__info__size span').html($('.select-size').val());
  newItem.find('.shopping-cart__item__info__color span').html($('.select-color').val());
  newItem.find('.shopping-cart__item__info__qty span').html($('.select-quantity').val());

  $('#cart-list').append(newItem);
  // console.log('hi');
  updateCart();

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
