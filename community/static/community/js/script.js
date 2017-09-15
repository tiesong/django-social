$(document).ready(function () {

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

    /* Assign the urls to share the profile to the social */
    var profile_url = window.location.href;
    $('.profile-social-share .twitter').attr('href', 'https://twitter.com/home?status='+profile_url);
    $('.profile-social-share .facebook').attr('href', 'https://www.facebook.com/sharer/sharer.php?u='+profile_url);
    $('.profile-social-share .email').attr('href', 'mailto:?&body='+profile_url);
    $('.profile-social-share .linkedin').attr('href', 'https://www.linkedin.com/shareArticle?mini=true&url='+profile_url);

    /* Upload image on profile edit */
    $('#upload_avatar').on('change',function(){
        $('.trans-back').hide();
    });

    $('#upload_avatar').on('mouseenter',function(){
        $('.trans-back').show();
        $('#upload_avatar').css('cursor', 'pointer');
    });

    $('#upload_avatar').on('mouseleave',function(){
        $('.trans-back').hide();
        $('#upload_avatar').css('cursor', 'default');
    });

    /* Select Tags for Profile*/
    $.ajax({
        url: '/c/tags/',
        dataType: 'json',
        success: function(result) {
            var tags = new Bloodhound({
                datumTokenizer: Bloodhound.tokenizers.obj.whitespace('tag_name'),
                queryTokenizer: Bloodhound.tokenizers.whitespace,
                local: result
                // prefetch: '/c/tags',
            });

            $('.tags').tagsinput({
                itemValue: 'tag_id',
                itemText: 'tag_name',
                typeaheadjs: {
                    name: 'tags',
                    displayKey: 'tag_name',
                    source: tags
                }
            });
        },
    });

    var profile_id = $('#profile_id').val();
    $.ajax({
        url: '/c/tags/',
        data: {profile_id: profile_id},
        dataType: 'json',
        success: function(result) {
            $.each(result, function(key, value) {
                $('.tags').tagsinput('add', { "tag_id": value.tag_id, "tag_name": value.tag_name});
            });
        },
    });

    var company_id = $('#company_id').val();
    $.ajax({
        url: '/c/tags_company/',
        data: {company_id: company_id},
        dataType: 'json',
        success: function(result) {
            $.each(result, function(key, value) {
                $('.tags').tagsinput('add', { "tag_id": value.tag_id, "tag_name": value.tag_name});
            });
        },
    });

    /* Form Submission Prevent for Enterkey */
    $('#profile_edit_form').on('keyup keypress', function(e) {
        var keyCode = e.keyCode || e.which;
        if (keyCode === 13) {
            e.preventDefault();
            return false;
        }
    });
    
});
