/**
 * Created by python on 17-9-15.
 */

$(function () {
    var num = $('#num');
    var area = $('#area');
    var user = $('#user');
    // 找出当前地址的id值
    var cur_site_id = $('.current').find('span').html();

    // 用父级的代理代理自己input的click的点击事件
    $('.addrlist').delegate('input', 'click', function () {
        // 取出当前点击的下一个label里面的内容
        var data = $(this).next().html();
        $('.current').html(data);// 让当前地址显示的是点击按钮的地址
        // 取出当前地址的id值
        cur_site_id = $('.current').find('span').html();
        // 把当前地址的id值赋给表单的一个隐藏input
        $('#cur_site_id').val(cur_site_id);
        // 把点击按钮的值发送给后台current视图
        $.get('/user/current/', {'data': data}, function () {

        })
    });

    // 把当前登录用户的所有收货地址显示出来
    $.get('/user/add_addr/', function (data) {
        // 接收{'list':list}用data.list即可取出list
        // list = [{},{},{}]这样的格式，里面一个个字典是一个个收货地址信息
        var list = data.list;
        // 遍历list取出每个字典n,用标签的格式加上n对应的键即可显示出收货地址的效果和样式
        $.each(list, function (i, n) {
            $('.addrlist').append('<dd>' +
                '<input type="radio" name="site">' +
                '<label>' +
                '<span style="display: none">' +
                '' + n.id + '</span>' +
                '&nbsp;' + n.addr + '&nbsp;&nbsp;&nbsp;(' + n.name + '&nbsp;' + '收)&nbsp;&nbsp;&nbsp;' + n.num + '&nbsp;&nbsp;&nbsp;' + '' +
                '<a href="#" class="a">修改</a>' +
                '<label>' +
                '</dd>')
        })
    });


    $('.addrlist,.current').delegate('a', 'click', function () {
        // 取出当前地址的id值
        cur_site_id = $('.current').find('span').html();
        // 把当前地址的id值赋给表单的一个隐藏input
        $('#cur_site_id').val(cur_site_id);
        // 取出当前点击修改的父级label找出span标签里面的id值
        var ad_id = $(this).parent().find('span').html();
        // 把当前点击修改的id传到xiugai视图中
        $.get('/user/xiugai/', {'ad_id': ad_id}, function (data) {
            // 取出当前地址的id值
            cur_site_id = $('.current').find('span').html();
            // 把点击修改的地址显示在编辑地址对应的输入框中
            $('#user').val(data.uuname);
            $('#area').val(data.uaddress);
            $('#num').val(data.uphone);
            $('#adid').val(ad_id);  // 当前点击的id值
            $('#cur_site_id').val(cur_site_id);  //　始终是当前地址的id值

        });

        // 把当前地址的id值赋给表单的一个隐藏input
        $('#cur_site_id').val(cur_site_id);


    });
    // 请求视图取出存在session的地址显示为当前地址
    $.get('/user/site_cur/', function (data) {
        var data = data.data;
        $('.current').html(data);


    });

});




