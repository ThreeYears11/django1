/**
 * Created by python on 17-9-15.
 */

$(function () {
    var num = $('#num');
    var area = $('#area');
    var user = $('#user');
    $('.info_submit').click(function () {
        var num_val = num.val();
        var area_val = area.val();
        var user_val = user.val();
        if (num_val == '' || area_val == '' || user_val == '') {
            $('#site').submit(function () {
                return false
            })
        }else{
            $.get('/user/add_addr/',function (data) {
                var list = data.list;
                $.each(list,function (i,n) {
                    $('.addrlist').append('<dd><input type="radio" name="site"><label>&nbsp;' + n.addr +'&nbsp;&nbsp;&nbsp;('+ n.name +'&nbsp;'+'收)&nbsp;&nbsp;&nbsp;'+ n.num + '&nbsp;&nbsp;&nbsp;'+'<a href="#">修改<label></dd>')
                })
            })
        }
    });
    $('.addrlist').delegate('input','click',function () {
        var data = $(this).next().html();
        $('.current').html(data);
        $.get('/user/current/',{'data':data},function () {

    })
    });
    $.get('/user/add_addr/',function (data) {
                var list = data.list;
                $.each(list,function (i,n) {
                    $('.addrlist').append('<dd>' +
                        '<input type="radio" name="site">' +
                        '<label>' +
                        '<span style="display: none">' +
                        ''+n.id+'</span>' +
                        '&nbsp;' + n.addr +'&nbsp;&nbsp;&nbsp;('+ n.name +'&nbsp;'+'收)&nbsp;&nbsp;&nbsp;'+ n.num + '&nbsp;&nbsp;&nbsp;'+'' +
                        '<a href="#" class="a">修改</a>' +
                        '<label>' +
                        '</dd>')
                })
            });

    $.get('/user/show_user/', function (data) {
        $('.login_btn').hide();
        $('.login_info').children().html(data.name);
        $('.login_info').show();

    });
    $.get('/user/site_cur/',function (data) {
        var data = data.data;
        $('.current').html(data);
    });
    $('.addrlist,.current').delegate('a','click',function (){

        var ad_id = $(this).parent().find('span').html();
        $.get('/user/xiugai/',{'ad_id':ad_id}, function (data) {
            $('#user').val(data.uuname);
            $('#area').val(data.uaddress);
            $('#num').val(data.uphone);
            $('#adid').val(ad_id)

        });

    });


});

