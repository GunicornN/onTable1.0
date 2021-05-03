$(document).ready(function()){
    $('.updateButton').on('click',function()){
        var member_id =  $(this).attr('member_id');
        var name

        req  = $.ajax({
            url : '/update',
            type : 'POST',
            data : {}

        });

        req.done(function(data)){
            $('#orderSection'+order.id).fadeOut(1000).fadeIn(1000);
            $('#orderSection'+order.id).text(data.member_num)
        });

    }


});
