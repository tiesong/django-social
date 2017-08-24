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

    // Booking Delete Action
    $('#deleteModal').on('show.bs.modal', function(e) {
        $(this).find('#delete').attr('href', $(e.relatedTarget).data('href'));
    });

    $('#delete').click(function(e) {
        e.preventDefault();
        var handler = $(this).attr('href');
        $.post(handler);
        document.location.reload();
    });

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // DataTables
    $('#bookings_table').DataTable();

    // DateTimepicker
    $('#time_start').datetimepicker({
        autoclose: true,
        minuteStep: 30,
        showMeridian: true,
    });
    $('#time_end').datetimepicker({
        autoclose: true,
        minuteStep: 30,
        showMeridian: true,
    });

    // Booking create
    $('#bookings_table .actions button#book_room').click(function() {
        room_id = $(this).parent('.actions').find('#room_id').val();
        date_start = $('#time_start').val();
        date_end = $('#time_end').val();
        if (date_start == '') {
            alert('You should enter the start time.')
            $('#time_start').focus();
        } else if (date_end == '') {
            alert('You should enter the end time.')
            $('#time_end').focus();
        }
        if (date_start != '' && date_end != '') {
            $.post('/officespace/create',
                {
                    room_id: room_id,
                    date_start: date_start,
                    date_end: date_end
                },
                function(result) {
                    if (result == 'success') {
                        $('#createModal').modal('show');
                        window.setTimeout(function(){
                            window.location.href = "/officespace";
                        }, 5000);
                    } else {

                    }
                }
            );
        }
    });

    // Booking Create by Room
    $('#calendar').fullCalendar({
        defaultView: 'agendaWeek',
    });

    // Booking Option Change
    $('.bookings-action .start-over').click(function() {
        if ($('.booking .choose-time').css('display') == 'none') {
            $('.bookings-option .choose-room').css('opacity', '0.3');
            $('.bookings-option .choose-time').css('opacity', '1');
            $('.bookings-option .choose-room select').attr('disabled', true);
            $('.bookings-option .choose-time .form-group input').attr('disabled', false);
            $('.booking .choose-room').hide();
            $('.booking .choose-time').show();
        } else if ($('.booking .choose-room').css('display') == 'none') {
            $('.bookings-option .choose-time').css('opacity', '0.3');
            $('.bookings-option .choose-room').css('opacity', '1');
            $('.bookings-option .choose-time .form-group input').attr('disabled', true);
            $('.bookings-option .choose-room select').attr('disabled', false);
            $('.booking .choose-time').hide();
            $('.booking .choose-room').show();
        }
    });

});
