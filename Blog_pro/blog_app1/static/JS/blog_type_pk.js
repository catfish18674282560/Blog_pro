$(function(){
    var $ul = $('.my_blog_pag ul');           // 获取ul标签
    var $li = $('.my_blog_pag ul li');        // 获取所有li标签

    $ul_width = $li.length * $li.width() + $li.length * 2;
    $ul.width($ul_width);

    $ul.css({
        marginLeft: $ul.offset().left - ($ul_width/2)
    })
});