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
    var booking_table = $('#bookings_table').DataTable({
        "order": [[ 0, "desc" ]]
    });

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
    $('#bookings_table .actions button').click(function() {
        room_id = $(this).parent('.actions').find('.room-id').val();
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
            var title = prompt('Booking Title:');
            if (title) {
                $.ajax({
                    url: '/officespace/create',
                    type: 'POST',
                    dataType: 'json',
                    data: {
                        room_id: room_id,
                        date_start: date_start,
                        date_end: date_end,
                        title: title
                    },
                    success: function(result) {
                        var room = result[0];
                        var title = result[1];
                        var start = result[2];
                        var end = result[3];
                        $('#createModal .modal-body .title').html(title);
                        $('#createModal .modal-body .time').html(start + ' - ' + end);
                        $('#createModal .modal-body .room').html(room);
                        $('#createModal').modal('show');
                        window.setTimeout(function(){
                            window.location.href = "/officespace";
                        }, 5000);
                    },
                    error: function(e) {
                        console.log(e);
                    }
                });
            } else {
                alert('You should enter the Booking Title.');
            }
        }
    });

    // Booking Create by Room
	var calendar = $('#calendar').fullCalendar({
        defaultView: 'agendaWeek',
        selectable: true,
        selectHelper: true,
        select: function(start, end, allDay)
        {
            if ($('.bookings-option #search_room').val() == '') {
                calendar.fullCalendar('option', 'selectable', false);
                return;
            } else {
                calendar.fullCalendar('option', 'selectable', true);
            }
            var title = prompt('Booking Title:');
            if (title)
            {
                calendar.fullCalendar('renderEvent',
                    {
                        title: title,
                        start: start,
                        end: end,
                        allDay: false,
                        editable: true,
                        color: '#4cc5f7',
                        className: 'new-booking'
                    },
                    false
                );
            }
            calendar.fullCalendar('unselect');
        },
        editable: false,
        allDaySlot: false,
        eventRender: function(event, element) {
            if (element.hasClass('new-booking')) {
                start_date = moment(event.start._d).format();
                end_date = moment(event.end._d).format();
                title = event.title;
                new_button = '<button type="button" class="btn btn-default book-room">Book Room</button>';
                element.append(new_button);
                $(element).find('button').click(function() {
                    room_id = $('.bookings-option #search_room').val();
                    if (start_date != '' && end_date != '') {
                        $.ajax({
                            url: '/officespace/create',
                            type: 'POST',
                            dataType: 'json',
                            data: {
                                room_id: room_id,
                                date_start: start_date,
                                date_end: end_date,
                                title: title
                            },
                            success: function(result) {
                                var room = result[0];
                                var title = result[1];
                                var start = result[2];
                                var end = result[3];
                                $('#createModal .modal-body .title').html(title);
                                $('#createModal .modal-body .time').html(start + ' - ' + end);
                                $('#createModal .modal-body .room').html(room);
                                $('#createModal').modal('show');
                                window.setTimeout(function(){
                                    window.location.href = "/officespace";
                                }, 5000);
                            },
                            error: function(e) {
                                console.log(e);
                            }
                        });
                    }
                });
            }
        },
        events: function(start, end, timezone, callback) {
            room_id = $('.bookings-option #search_room').val();
            start_book = moment(start._d).format();
            end_book = moment(end._d).format();
            var events = [];
            if (room_id != '') {
                $.ajax({
                    url: '/officespace/create',
                    dataType: 'json',
                    data: {
                        room_id: room_id,
                        start_book: start_book,
                        end_book: end_book
                    },
                    success: function(result) {
                        $.each(result, function(index, value) {
                            if (value[0] == 'true') {
                                events.push({
                                    title: value[1],
                                    start: value[2],
                                    end: value[3],
                                    allDay: false,
                                    color: '#4cc5f7'
                                });
                            } else {
                                events.push({
                                    title: value[1],
                                    start: value[2],
                                    end: value[3],
                                    allDay: false,
                                });
                            }
                        });
                        callback(events);
                    },
                    error: function(e) {
                        console.log(e);
                    }
                });
            } else {
                callback(events);
            }
        }
    });
    $('.bookings-option #search_room').change(function() {
        $('#calendar').fullCalendar( 'refetchEvents' );
        calendar.fullCalendar('option', 'selectable', true);
    });

    // Booking Option Change
    $('.bookings-action .start-over').click(function() {
        if ($('.booking .choose-time').css('display') == 'none') {
            $('.bookings-option .choose-room').css('opacity', '0.3');
            $('.bookings-option .choose-time').css('opacity', '1');
            $('.bookings-option .choose-room select').attr('disabled', true);
            $('.bookings-option .choose-room select').val('');
            $('.bookings-option .choose-time .form-group input').attr('disabled', false);
            $('.booking .choose-room').hide();
            $('.booking .choose-time').show();
        } else if ($('.booking .choose-room').css('display') == 'none') {
            $('.bookings-option .choose-time').css('opacity', '0.3');
            $('.bookings-option .choose-room').css('opacity', '1');
            $('.bookings-option .choose-time .form-group input').attr('disabled', true);
            $('.bookings-option .choose-time .form-group input#time_start').val('');
            $('.bookings-option .choose-time .form-group input#time_end').val('');
            $('.bookings-option .choose-room select').attr('disabled', false);
            $('.booking .choose-time').hide();
            $('.booking .choose-room').show();
        }
    });

    // Search Room for Booking
    // $('.choose-time #search_time').click(function() {
    //     date_start = $('#time_start').val();
    //     date_end = $('#time_end').val();
    //     if (date_start == '') {
    //         alert('You should enter the start time.')
    //         $('#time_start').focus();
    //     } else if (date_end == '') {
    //         alert('You should enter the end time.')
    //         $('#time_end').focus();
    //     }
    //     if (date_start != '' && date_end != '') {
    //         $.ajax({
    //             url: '/officespace/create',
    //             dataType: 'json',
    //             data: {
    //                 date_start: date_start,
    //                 date_end: date_end,
    //                 type: 'search'
    //             },
    //             success: function(result) {
    //                 console.log(result);
    //                 var table = '<thead><tr><th></th><th>Info</th><th>Action</th><th></th></tr></thead>' +'<tbody>';
    //                 $.each(result, function(index, value) {
    //                     table += '<tr style="background: #f9f9f9;"><td><span style="display: none;">'+ value.id + '</span></td><td><p>Space // '+ value.category + '</p><h2>'+ value.name + '</h2></td><td class="actions text-right" style="vertical-align: middle;"><input type="hidden" class="room-id" value="'+ value.id + '" /><buttontype="button" class="btn btn-default">Book Room</button></td><td></td></tr>';
    //                 })
    //                 table += '</tbody>';
    //                 $('#bookings_table').html(table);
    //             },
    //             error: function(e) {
    //                 console.log(e);
    //             }
    //         });
    //         booking_table.fnDraw();
    //     }
    // });

});
