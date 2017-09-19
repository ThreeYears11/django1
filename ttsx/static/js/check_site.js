/**
 * Created by python on 17-9-17.
 */


$(function(){
	$('#user').next().hide();
	$('#area').next().hide();
	$('#num').next().hide();
	var error_name = false;
	var error_phone = false;
	var error_site= false;


	$('#user').blur(function() {
		check_user_name();
	});
	$('#area').blur(function () {
		check_area();
    });

	$('#num').blur(function() {
		check_phone();
	});
	$('#user').focus(function() {
		$('#user').next().hide();
	});
	$('#area').focus(function() {
		$('#area').next().hide();
	});
	$('#num').focus(function() {
		$('#num').next().hide();
	});



	function check_user_name(){
		var len = $('#user').val().length;
		if(len==0){
			$('#user').next().html('* 收获姓名不能为空');
			$('#user').next().show();
			error_name = true;
		}
		else if(len>20)
		{
			$('#user').next().html('* 长度不超过20个字符');
			$('#user').next().show();
			error_name = true;
		}
		else
		{
			$('#user').next().hide();
			error_name = false;
		}
	}

	function check_area(){
		var len = $('#area').val().length;
		if(len==0){
			$('#area').next().html('* 收获地址不能为空');
			$('#area').next().show();
			error_site = true;
		}
		else if(len<8)
		{
			$('#area').next().html('* 亲，为了您的宝贝早日到达，请详细填写地址');
			$('#area').next().show();
			error_site = true;
		}
		else
		{
			$('#area').next().hide();
			error_site = false;
		}
	}




	function check_phone(){
		var len = $('#num').val().length;
		if(len==0){
			$('#num').next().html('* 手机号码不能为空');
			$('#num').next().show();
			error_phone = true;
		}
		else if(len == 11)
		{
			$('#num').next().hide();
			error_phone = false;
		}
		else
		{
			$('#num').next().html('* 请输入正确位数的手机号码');
			$('#num').next().show();
			error_phone = true;
		}

	}


	$('#site').submit(function() {
		check_user_name();
		check_area();
		check_phone();

		if(error_name == false && error_phone == false && error_site == false)
		{
			return true;
		}
		else
		{
			return false;
		}

	});








});