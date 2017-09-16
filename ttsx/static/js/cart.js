/**
 * Created by python on 17-9-14.
 */
        $(function () {
            $('.good_id').hide()  //{# 用来传商品的id #}
            // {# 页面刷新出来时商品的数量 #}
            var number = 0
            $('.cart_con ul').each(function () {
                number += 1
            })
            $('.total_count em').html(number)
            $('.settlements .col03 b').html(number)


            $('.cart_con ul').each(function () {
                // 删除的点击效果
                $('.cart_list_td .col08 a').click(function () {
                    var good_id = $(this).parent().siblings('.good_id').html()
                    $.get('/cart/delete_data/',{'good_id':good_id,'user_id':1})
                    $(this).parent().parent().remove()
                    var all_price = 0
                    var n1 = 0
                    var n2 = 0
                    $('.cart_con ul').each(function () {
                        // 计算结算金额
                        var fuhao = 0
                        var single_price = parseFloat($(this).find('.col07').html())
                        var a = $(this).children('.col01').children().prop('checked')
                        if (a == true) {
                            fuhao = 1
                        }
                        all_price += single_price*fuhao
                        n1 += 1
                        n2 += fuhao
                    })
                    $('.settlements .col03 em').html(all_price.toFixed(2))
                    $('.total_count em').html(n1)
                    $('.settlements .col03 b').html(n2)
                })

                var n = 0
                var price = parseFloat($(this).find('.price').html())
                var num = parseFloat($(this).find('.num_show').val())
                var sum_price = price * num
                $(this).find('.col07').html(sum_price.toFixed(2) + '元')
                //{# check的点击效果 #}
                $(this).find('.col01').click(function () {
                    var str = 0
                    var n = 0
                    $('.cart_con ul').each(function () {
                        var fuhao = 0
                        var a = $(this).find('.col01').children().prop('checked')
                        if (a == true) {
                            fuhao = 1
                        }
                        n += fuhao
                        var b = parseFloat($(this).find('.col07').html())
                        str += b*fuhao
                    })
                    $('.settlements .col03 b').html(n)
                    $(this).parent().parent().next().children('.col03').children('em').html(str.toFixed(2))
                })
                // {# 加号的点击效果#}
                $(this).find('.add').click(function () {
                    // {# 修改数据库中的值 #}
                    var good_id = $(this).parent().parent().siblings('.good_id').html()
                    var count = $(this).next().val()
                    $.get('/cart/change_data1/',{'good_id':good_id,'user_id':1,'count':count})
                    // {#-------------------------------------------#}
                    var value = parseInt($(this).next().val())
                    value += 1
                    $(this).next().val(value)
                    // {# 动态修改小计金额#}
                    var price = parseFloat($(this).parent().parent().prev().children().html())
                    var num = parseFloat($(this).next().val())
                    var sum_price = price * num
                    $(this).parent().parent().next().html(sum_price.toFixed(2) + '元')
                   // {# 计算结算金额#}
                    var all_price = 0
                    $('.cart_con ul').each(function () {
                        var fuhao = 0
                        var single_price = parseFloat($(this).find('.col07').html())
                        var a = $(this).children('.col01').children().prop('checked')
                        if (a == true) {
                            fuhao = 1
                        }
                        all_price += single_price*fuhao
                    })
                    $(this).parent().parent().parent().parent().next().children('.col03').children('em').html(all_price.toFixed(2))

                })
                // {# 减号的点击效果#}
                $(this).find('.minus').click(function () {
                    // {# 修改数据库中的值 #}
                    var good_id = $(this).parent().parent().siblings('.good_id').html()
                    var count = $(this).prev().val()
                    $.get('/cart/change_data2/',{'good_id':good_id,'user_id':1,'count':count})
                    // {#-------------------------------------------#}
                    var value = parseInt($(this).prev().val())
                    value -= 1
                    if (value != -1) {
                        $(this).prev().val(value)
                    }
                    // {#动态修改小计金额#}
                    var price = parseFloat($(this).parent().parent().prev().children().html())
                    var num = parseFloat($(this).prev().val())
                    var sum_price = price * num
                    $(this).parent().parent().next().html(sum_price.toFixed(2) + '元')
                    // {# 计算结算金额#}
                    var all_price = 0
                    $('.cart_con ul').each(function () {
                        var fuhao = 0
                        var single_price = parseFloat($(this).find('.col07').html())
                        var a = $(this).children('.col01').children().prop('checked')
                        if (a == true) {
                            fuhao = 1
                        }
                        all_price += single_price*fuhao
                    })
                    $(this).parent().parent().parent().parent().next().children('.col03').children('em').html(all_price.toFixed(2))

                })

            })


            // {# 页面刚刷新出来时的结算金额 #}
            var total_price = 0
            $('.cart_con ul').each(function () {
                var line_price = parseFloat($(this).find('.col07').html())
                total_price += line_price
            })
            $('.settlements .col03 em').html(total_price.toFixed(2))
         // {# 全选的点击效果 #}
        $('.settlements .col01').click(function () {
            var all_pick = $(this).children().prop('checked')
            if (all_pick == true) {
                $('.cart_con ul').each(function () {
                    $(this).find('.col01').children().prop('checked',true)
                })
            }else {
                $('.cart_con ul').each(function () {
                    $(this).find('.col01').children().prop('checked',false)
                })
            }
            var all_price = 0
            var n = 0
            $('.cart_con ul').each(function () {
                var fuhao = 0
                var single_price = parseFloat($(this).find('.col07').html())
                var a = $(this).children('.col01').children().prop('checked')
                if (a == true) {
                    fuhao = 1
                }
                all_price += single_price*fuhao
                n += fuhao
            })
            $(this).siblings('.col03').children('em').html(all_price.toFixed(2))
            $('.settlements .col03 b').html(n)
        })

            //input 的change事件
            $('.cart_con ul').each(function () {


                $('.num_show').bind('input',function () {
                    // {# 修改数据库中的值 #}
                    var good_id = $(this).parent().parent().siblings('.good_id').html()
                    var count = $(this).val()-1
                    $.get('/cart/change_data1/',{'good_id':good_id,'user_id':1,'count':count})
                    // {# 动态修改小计金额#}
                    var number = parseInt($(this).val())
                    if ($('.num_show').val()=='') {
                        number = 0
                    }
                    var price = parseFloat($(this).parent().parent().prev().children().html())
                    var sum_price = price * number
                    $(this).parent().parent().next().html(sum_price.toFixed(2) + '元')
                    // 动态计算结算金额
                    var all_price = 0
                    $('.cart_con ul').each(function () {
                        var fuhao = 0
                        var single_price = parseFloat($(this).find('.col07').html())
                        var a = $(this).children('.col01').children().prop('checked')
                        if (a == true) {
                            fuhao = 1
                        }
                        all_price += single_price*fuhao
                    })
                    var a = $(this).parent().parent().parent().parent().next().find('.col03').children('em').html(all_price.toFixed(2))
                    console.log(a)
                })
            })
        })