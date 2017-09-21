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

    /* Form Submission Prevent for Enterkey */
    $('#profile_edit_form').on('keyup keypress', function(e) {
        var keyCode = e.keyCode || e.which;
        if (keyCode === 13) {
            e.preventDefault();
            return false;
        }
    });

    $.ajax({
        url: '/c/list_companies/',
        dataType: 'json',
        success: function (result) {
            var tags = new Bloodhound({
                datumTokenizer: Bloodhound.tokenizers.whitespace,
                queryTokenizer: Bloodhound.tokenizers.whitespace,
                local: result
            });

            console.log(result);
            $('.companytags').tagsinput({
                typeaheadjs: {
                    name: 'tags',
                    source: tags
                },
                freeInput: true
            });
        },
    });

});
