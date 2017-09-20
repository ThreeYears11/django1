/**
 * Created by python on 17-9-15.
 */

$(function () {
    var num = $('#num');
    var area = $('#area');
    var user = $('#user');
    var cur_site_id = $('.current').find('span').html();

    $('.addrlist').delegate('input','click',function () {
        var data = $(this).next().html();
        $('.current').html(data);
        cur_site_id = $('.current').find('span').html();
        $('#cur_site_id').val(cur_site_id);
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



    $('.addrlist,.current').delegate('a','click',function (){
        cur_site_id = $('.current').find('span').html();
        $('#cur_site_id').val(cur_site_id);
        var ad_id = $(this).parent().find('span').html();
        $.get('/user/xiugai/',{'ad_id':ad_id}, function (data) {
            cur_site_id = $('.current').find('span').html();
            $('#user').val(data.uuname);
            $('#area').val(data.uaddress);
            $('#num').val(data.uphone);
            $('#adid').val(ad_id);
            $('#cur_site_id').val(cur_site_id);

        });

    // $('#site').append('<div class="form_group"> <input type="hidden" name="cur_site_id" id="cur_site_id" ></div>');
        $('#cur_site_id').val(cur_site_id);


    });
     $.get('/user/site_cur/',function (data) {
        var data = data.data;
        $('.current').html(data);



    });

});




