$(document).ready(function(){
    $(".small_img").hover(function(){
        var img_url = $(this).attr('src');
        var img_elem = $('<img>').attr('src', img_url);
        $(this).closest('.box_main').find('.box_img').empty().append(img_elem);
    });
 });