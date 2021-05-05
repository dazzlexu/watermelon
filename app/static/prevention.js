$(function () {
    $('li').mouseover(function (e) {
        $(this).siblings().stop().fadeTo(2000, 0.0); /*鼠标触碰图片渐变消失*/
    });
    $('li').mouseout(function (e) {
        $(this).siblings().stop().fadeTo(2000, 1); /*鼠标触碰图片变明*/
    });
})