$(function () {

    /* Toggle responsive menu */
    $('#toggle-menu').click(function() {
        if(!$(this).hasClass('close')) {
            $('#toggle-menu').addClass('close');
            $('.site-navigation').addClass('show');
            $('body').css('overflow', 'hidden');
        } else {
            $('.site-navigation').removeClass('show');
            $('#toggle-menu').removeClass('close');
            $('body').css('overflow', 'auto');
        }
    });

    if($('.filters-wrapper').length > 0) {
        $('.filters-wrapper').affix({
            offset: {
               top: $('.filters-wrapper').offset().top
            }
        });
    }

    var profile_url = window.location.href;
    $('.profile-social-share .twitter').attr('href', 'https://twitter.com/home?status='+profile_url);
    $('.profile-social-share .facebook').attr('href', 'https://www.facebook.com/sharer/sharer.php?u='+profile_url);
    $('.profile-social-share .email').attr('href', 'mailto:?&body='+profile_url);
    $('.profile-social-share .linkedin').attr('href', 'https://www.linkedin.com/shareArticle?mini=true&url='+profile_url);

    $('#upload_avatar').on('change',function(){
        $('.trans-back').hide();
    });

    $('#upload_avatar').on('mouseenter',function(){
        $('.trans-back').show();
    });

    $('#upload_avatar').on('mouseleave',function(){
        $('.trans-back').hide();
    });

});
