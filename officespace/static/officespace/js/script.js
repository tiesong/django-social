$(document).ready(function () {

    /* Toggle responsive menu */
    $('#toggle-menu').click(function () {
        if (!$(this).hasClass('close')) {
            $('#toggle-menu').addClass('close');
            $('.site-navigation').addClass('show');
            $('body').css('overflow', 'hidden');
        } else {
            $('.site-navigation').removeClass('show');
            $('#toggle-menu').removeClass('close');
            $('body').css('overflow', 'auto');
        }
    });

    if ($('.filters-wrapper').length > 0) {
        $('.filters-wrapper').affix({
            offset: {
                top: $('.filters-wrapper').offset().top
            }
        });
    }

    // Booking Delete Action
    $('#deleteModal').on('show.bs.modal', function (e) {
        $(this).find('#delete').attr('href', $(e.relatedTarget).data('href'));
    });

    $('#delete').click(function (e) {
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
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // DataTables
    var booking_table = $('#bookings_table').DataTable({
        "order": [[0, "desc"]]
    });

    // DateTimepicker
    // $('#time_start').datetimepicker({
    //     autoclose: true,
    //     minuteStep: 30,
    //     showMeridian: true,
    // });
    // $('#time_end').datetimepicker({
    //     autoclose: true,
    //     minuteStep: 30,
    //     showMeridian: true,
    // });

    $('.booking .choose-room').show();
    // Booking Create by Time
    $('#bookings_table .actions button').click(function () {
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
                    success: function (result) {
                        var room = result[0];
                        var title = result[1];
                        var start = result[2];
                        var end = result[3];
                        if (start.indexOf('T') > 0) {
                            start_ = start.replace(/\+.*/g, ' UTC');
                            _start = start.replace(/[^\dT]/g, '').replace('0000', '');
                        } else {
                            start_ = start + ' UTC';
                            _start = start.replace(/-(\d+)\s/g, '$1T').replace(/[^\dT]/g, '') + '00';
                        }
                        if (end.indexOf('T') > 0) {
                            end_ = end.replace(/\+.*/g, ' UTC');
                            _end = end.replace(/[^\dT]/g, '').replace('0000', '');
                        } else {
                            end_ = end + ' UTC';
                            _end = end.replace(/-(\d+)\s/g, '$1T').replace(/[^\dT]/g, '') + '00';
                        }
                        var google_link = 'https://www.google.com/calendar/render?action=TEMPLATE' +
                            '&text=' + title +
                            '&details=Room: ' + room +
                            '&location=Your Butter Factory' +
                            '&dates=' + _start + '/' + _end;
                        var iCal_link = 'http://addtocalendar.com/atc/ical?f=m' +
                            '&e[0][date_start]=' + _start +
                            '&e[0][date_end]=' + _end +
                            '&e[0][timezone]=UTC' +
                            '&e[0][title]=' + title +
                            '&e[0][description]=Room: ' + room +
                            '&e[0][location]=Your Butter Factory' +
                            '&e[0][privacy]=public';
                        $('#createModal .modal-body .gCal').attr('href', google_link);
                        $('#createModal .modal-body .iCal').attr('href', iCal_link);
                        $('#createModal .modal-body .oCal').attr('href', iCal_link);
                        $('#createModal .modal-body .title').html(title);
                        $('#createModal .modal-body .time').html(start_ + ' - ' + end_);
                        $('#createModal .modal-body .room').html(room);
                        $('#createModal').modal('show');
                    },
                    error: function (e) {
                        console.log(e);
                    }
                });
            } else {
                alert('You should enter the Booking Title.');
            }
        }
    });

    $('.bookings-option #search_room').change(function () {
        $('#calendar').fullCalendar('refetchEvents');
        // calendar.fullCalendar('option', 'selectable', true);
    });

    //Booking Edit
    var edit_calendar = $('#edit_calendar').fullCalendar({
        header: {
            left: 'month,agendaWeek,agendaDay',
            center: 'title',
        },
        defaultView: 'agendaWeek',
        dayOfMonthFormat: 'ddd D/M',
        eventLimit: true,
        selectable: true,
        selectHelper: true,
        select: function (start, end, allDay) {
            if ($('.bookings-option #search_room').val() == '') {
                edit_calendar.fullCalendar('option', 'selectable', false);
                return;
            } else if ($('.booking-edit .bookings-action button.title-change').hasClass('showing')) {
                return;
            } else {
                edit_calendar.fullCalendar('option', 'selectable', true);
            }
            var title = prompt('Booking Title:');
            if (title) {
                edit_calendar.fullCalendar('renderEvent',
                    {
                        title: title,
                        start: start,
                        end: end,
                        allDay: false,
                        editable: true,
                        color: '#4cc5f7',
                        className: 'edit-booking'
                    },
                    false
                );
            }
            edit_calendar.fullCalendar('unselect');
        },
        editable: false,
        allDaySlot: false,
        eventOverlap: false,
        selectOverlap: false,
        longPressDelay: 300,
        eventRender: function (event, element) {
            if (element.hasClass('edit-booking')) {
                var booking_id = $('.booking-edit #booking_id').val();
                var room_id = $('.bookings-option #search_room').val();
                var start_date = moment(event.start._d).tz("UTC").format();
                var end_date = moment(event.end._d).tz("UTC").format();
                var event_title = event.title;
                if (event.id && event.id == booking_id) {
                    var new_button = '<button type="button" class="pull-right btn btn-transparent-dark showing title-change">Edit Title</button><button type="button" class="pull-right btn btn-transparent-dark edit-room">Save Book</button>';
                } else {
                    var new_button = '<button type="button" class="pull-right btn btn-transparent-dark title-change">Edit Title</button><button type="button" class="pull-right btn btn-transparent-dark edit-room">Save Book</button>';
                }
                $('.booking-edit .bookings-action .title-change').remove();
                $('.booking-edit .bookings-action .edit-room').remove();
                $(new_button).insertBefore('.booking-edit .bookings-action .clearfix');
                $('.booking-edit .bookings-action button.title-change').click(function () {
                    var title = prompt('Booking Title:');
                    if (title) {
                        event_title = title;
                        event.title = title;
                        $('#edit_calendar').fullCalendar('updateEvent', event);
                    }
                });
                $('.booking-edit .bookings-action button.edit-room').click(function () {
                    if (start_date != '' && end_date != '') {
                        $.ajax({
                            url: '/officespace/' + booking_id + '/edit/',
                            type: 'POST',
                            dataType: 'json',
                            data: {
                                booking_id: booking_id,
                                room_id: room_id,
                                date_start: start_date,
                                date_end: end_date,
                                title: event_title
                            },
                            success: function (result) {
                                var room = result[0];
                                var title = result[1];
                                var start = result[2];
                                var end = result[3];
                                if (start.indexOf('T') > 0) {
                                    start_ = start.replace(/\+.*/g, ' UTC');
                                    _start = start.replace(/[^\dT]/g, '').replace('0000', '');
                                } else {
                                    start_ = start + ' UTC';
                                    _start = start.replace(/-(\d+)\s/g, '$1T').replace(/[^\dT]/g, '') + '00';
                                }
                                if (end.indexOf('T') > 0) {
                                    end_ = end.replace(/\+.*/g, ' UTC');
                                    _end = end.replace(/[^\dT]/g, '').replace('0000', '');
                                } else {
                                    end_ = end + ' UTC';
                                    _end = end.replace(/-(\d+)\s/g, '$1T').replace(/[^\dT]/g, '') + '00';
                                }
                                var google_link = 'https://www.google.com/calendar/render?action=TEMPLATE' +
                                    '&text=' + title +
                                    '&details=Room: ' + room +
                                    '&location=Your Butter Factory' +
                                    '&dates=' + _start + '/' + _end;
                                var iCal_link = 'http://addtocalendar.com/atc/ical?f=m' +
                                    '&e[0][date_start]=' + _start +
                                    '&e[0][date_end]=' + _end +
                                    '&e[0][timezone]=UTC' +
                                    '&e[0][title]=' + title +
                                    '&e[0][description]=Room: ' + room +
                                    '&e[0][location]=Your Butter Factory' +
                                    '&e[0][privacy]=public';
                                $('#createModal .modal-body .gCal').attr('href', google_link);
                                $('#createModal .modal-body .iCal').attr('href', iCal_link);
                                $('#createModal .modal-body .oCal').attr('href', iCal_link);
                                $('#createModal .modal-body .title').html(title);
                                $('#createModal .modal-body .time').html(start_ + ' - ' + end_);
                                $('#createModal .modal-body .room').html(room);
                                $('#createModal').modal('show');
                            },
                            error: function (e) {
                                console.log(e);
                            }
                        });
                    }
                });
            }
        },
        events: function (start, end, timezone, callback) {
            var booking_id = $('.booking-edit #booking_id').val();
            var room_id = $('.bookings-option #search_room').val();
            var start_book = moment(start._d).tz("UTC").format();
            var end_book = moment(end._d).tz("UTC").format();
            var events = [];
            if (room_id != '') {
                $.ajax({
                    url: '/officespace/' + booking_id + '/edit',
                    dataType: 'json',
                    data: {
                        booking_id: booking_id,
                        room_id: room_id,
                        start_book: start_book,
                        end_book: end_book
                    },
                    success: function (result) {
                        $('.booking-create .bookings-action .book-room').remove();
                        $('.booking-edit .bookings-action .title-change').remove();
                        $('.booking-edit .bookings-action .edit-room').remove();
                        for (var i = 0; i < result.length; i++) {
                            if (result[i][4] == 'true') {
                                events.push({
                                    id: booking_id,
                                    title: result[i][1],
                                    start: result[i][2],
                                    end: result[i][3],
                                    allDay: false,
                                    color: '#4cc5f7',
                                    editable: true,
                                    className: 'edit-booking'
                                });
                            } else if (result[i][0] == 'true') {
                                events.push({
                                    title: result[i][1],
                                    start: result[i][2],
                                    end: result[i][3],
                                    allDay: false,
                                    color: '#4cc5f7'
                                });
                            } else {
                                events.push({
                                    title: 'unavailable',
                                    start: result[i][2],
                                    end: result[i][3],
                                    allDay: false,
                                });
                            }
                        }
                        callback(events);
                    },
                    error: function (e) {
                        console.log(e);
                    }
                });
            } else {
                $('.booking-edit .bookings-action .title-change').remove();
                $('.booking-edit .bookings-action .edit-room').remove();
                callback(events);
            }
        }
    });
    $('.bookings-option #search_room').change(function () {
        $('#edit_calendar').fullCalendar('refetchEvents');
        edit_calendar.fullCalendar('option', 'selectable', true);
    });

    // Confirmation modal
    $('#createModal .booking-confirm').click(function () {
        window.location.href = "/officespace";
    });

    // Booking Option Change
    $('.bookings-option .choose-time').click(create_booking());

    var calendar = {};

    $('.bookings-action .start-over').click(function () {
        window.location.href = "/officespace/create";
    });

    $(".chosen-select").chosen({
        no_results_text: "Oops, nothing found!"
    });
    $(".chosen-select").chosen().change(function (ev, data) {

    });

});

function create_booking() {

    $('.booking .choose-room').show();

    /* Booking Create by Room */
    calendar = $('#calendar').fullCalendar({
        header: {
            left: 'month,agendaWeek,agendaDay',
            center: 'title'
        },
        defaultView: 'agendaWeek',
        dayOfMonthFormat: 'ddd D/M',
        eventLimit: true,
        selectable: true,
        selectHelper: true,
        select: function (start, end, allDay) {
            if ($('.fc-event-container .showing').hasClass('showing')) {
                return;
            } else {
                console.log('selectable True');
                calendar.fullCalendar('option', 'selectable', true);
            }
            calendar.fullCalendar('renderEvent',
                {
                    id: '12345',
                    start: start,
                    end: end,
                    allDay: false,
                    editable: true,
                    color: '#4cc5f7',
                    className: 'new-booking showing'
                },
                false
            );
            calendar.fullCalendar('unselect');
        },
        editable: false,
        allDaySlot: false,
        eventOverlap: false,
        selectOverlap: false,
        longPressDelay: 300,
        eventRender: function (event, element) {
            if (element.hasClass('new-booking')) {
                var start_date = moment(event.start._d).tz("UTC").format();
                var end_date = moment(event.end._d).tz("UTC").format();

                $('#titleModal').modal('show');

                $('#titleModal').on('hidden.bs.modal', function () {
                    if (!$(this).data('created'))
                        calendar.fullCalendar('removeEvents', '12345');
                    // $("#titleModal").remove();
                });

                $('#booking_create').click(function () {
                    var title = $('#bookingTitle').val();
                    if (title == '') {
                        alert('Please enter the Title.');
                        return;
                    }
                    $('#titleModal').data('created', true);
                    $('#titleModal').modal('hide');
                    var room_id = $('#selectRoom').val();
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
                            success: function (result) {
                                var room = result[0];
                                var title = result[1];
                                var start = result[2];
                                var end = result[3];
                                if (start.indexOf('T') > 0) {
                                    start_ = start.replace(/\+.*/g, ' UTC');
                                    _start = start.replace(/[^\dT]/g, '').replace('0000', '');
                                } else {
                                    start_ = start + ' UTC';
                                    _start = start.replace(/-(\d+)\s/g, '$1T').replace(/[^\dT]/g, '') + '00';
                                }
                                if (end.indexOf('T') > 0) {
                                    end_ = end.replace(/\+.*/g, ' UTC');
                                    _end = end.replace(/[^\dT]/g, '').replace('0000', '');
                                } else {
                                    end_ = end + ' UTC';
                                    _end = end.replace(/-(\d+)\s/g, '$1T').replace(/[^\dT]/g, '') + '00';
                                }
                                var google_link = 'https://www.google.com/calendar/render?action=TEMPLATE' +
                                    '&text=' + title +
                                    '&details=Room: ' + room +
                                    '&location=Your Butter Factory' +
                                    '&dates=' + _start + '/' + _end;
                                var iCal_link = 'http://addtocalendar.com/atc/ical?f=m' +
                                    '&e[0][date_start]=' + _start +
                                    '&e[0][date_end]=' + _end +
                                    '&e[0][timezone]=UTC' +
                                    '&e[0][title]=' + title +
                                    '&e[0][description]=Room: ' + room +
                                    '&e[0][location]=Your Butter Factory' +
                                    '&e[0][privacy]=public';
                                $('#createModal .modal-body .gCal').attr('href', google_link);
                                $('#createModal .modal-body .iCal').attr('href', iCal_link);
                                $('#createModal .modal-body .oCal').attr('href', iCal_link);
                                $('#createModal .modal-body .title').html(title);
                                $('#createModal .modal-body .time').html(start_ + ' - ' + end_);
                                $('#createModal .modal-body .room').html(room);
                                $('#createModal').modal('show');
                            },
                            error: function (e) {
                                console.log(e);
                                $('#titleModal').modal('hide');
                            }
                        });
                    }
                });
            }
        },
        events: function (start, end, timezone, callback) {
            var room_id = $('#search_room').val();
            var start_book = moment(start._d).tz("UTC").format();
            var end_book = moment(end._d).tz("UTC").format();
            var events = [];
            if (room_id != '') {
                $.ajax({
                    type: 'POST',
                    url: '/officespace/booking',
                    traditional: true,
                    dataType: 'json',
                    data: {
                        room_id: room_id.toString(),
                        start_book: start_book,
                        end_book: end_book
                    },
                    success: function (result) {
                        $.each(result, function (index, value) {
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
                                    title: 'unavailable',
                                    start: value[2],
                                    end: value[3],
                                    allDay: false
                                });
                            }
                        });
                        callback(events);
                    },
                    error: function (e) {
                        console.log(e);
                    }
                });
            } else {
                callback(events);
            }
        }
    });
}

