/**
 * Created by snake on 9/27/2017.
 */
$("#reminderTime").datetimepicker({
    format: 'yyyy-mm-dd hh:ii',
    autoclose: true,
    todayBtn: true
});

$(document).ready(function () {
    var news_url = window.location.href;
    $('.social-share .twitter').attr('href', 'https://twitter.com/home?status=' + news_url);
    $('.social-share .facebook').attr('href', 'https://www.facebook.com/sharer/sharer.php?u=' + news_url);
    $('.social-share .email').attr('href', 'mailto:?&body=' + news_url);
    $('.social-share .linkedin').attr('href', 'https://www.linkedin.com/shareArticle?mini=true&url=' + news_url);
})
