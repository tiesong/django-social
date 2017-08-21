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

    // DataTables
    $('#bookings_table').DataTable();
});
