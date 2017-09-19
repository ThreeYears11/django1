/**
 * Created by python on 17-9-16.
 */
$(function () {

    var error_name = false;
    var error_password = false;
    var error_yzm = false;

    $('#username').blur(function () {
        check_user_name();
    });

    $('#pwd').blur(function () {
        check_pwd();
    });
    $('#login_yzm').blur(function () {
        check_yzm();
    });

    function check_yzm() {

        $.get('/user/check_yzm/', {'yzm': $('#login_yzm').val()}, function (data) {
            if (data.yzm == 'ok') {
                error_yzm = false;
            } else {
                $('#login_yzm_img').next().html('验证码错误').show();
                error_yzm = true;
            }
        })
    }


    function check_user_name() {
        var len = $('#username').val().length;
        if (len < 5 || len > 20) {
            $('#username').next().html('请输入5-20个字符的用户名');
            $('#username').next().show();
            error_name = true;
        }
        else {
            $('#username').next().hide();
            error_name = false;

        }
    }

    function check_pwd() {
        var len = $('#pwd').val().length;
        if (len < 8 || len > 20) {
            $('#pwd').next().html('密码最少8位，最长20位');
            $('#pwd').next().show();
            error_password = true;
        }
        else {
            $('#pwd').next().hide();
            error_password = false;
        }
    }


    $('.myform').submit(function () {
        check_user_name();
        check_pwd();
        check_yzm();

        if (error_name == false && error_password == false && error_yzm == false) {
            return true;
        }
        else {
            return false;
        }

    });

})