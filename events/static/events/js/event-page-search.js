/**
 * Created by snake on 9/27/2017.
 */
var week_num;
var totalPage;
var method;
var value;
loading();
$(document).ready(function () {
    check_loading();
    week_num = 1;
    method = 'index';

    $('#search').click(function () {

        if ($("#search-form").is(':visible')) {
            $("#search-form").fadeOut();
        } else {
            $("#search-form").fadeIn();
        }
    });

    $('#search_top').click(function () {

        if ($("#search-form").is(':visible')) {
            $("#search-form").fadeOut();
        } else {
            $("#search-form").fadeIn();
        }
    });

    $(document.body).click(function (e) {
        //Hide the search bar if visible
        if (e.target.id !== "searchBar" && e.target.id !== "search" && e.target.id !== "search_top") {
            document.getElementById("searchBar").value = "";
            $("#search-form").hide();
        }
    });

    $("#startdatetime").datetimepicker({
        format: 'yyyy-mm-dd hh:ii',
        autoclose: true,
        todayBtn: true
    });

    $("#enddatetime").datetimepicker({
        format: 'yyyy-mm-dd hh:ii',
        autoclose: true,
        todayBtn: true
    });


});
function check_loading() {
    var everythingLoaded = setInterval(function () {
        if (document.readyState === 'complete') {
            clearInterval(everythingLoaded);
            loaded(); // this is the function that gets called when everything is loaded
        }
    }, 10);

}

function loaded() {
    console.log('loaded');
    $('.loader').hide();
    $("#article_list").show();

}

function loading() {
    $('.loader').show();
    $("#article_list").hide();
}



function newEvent() {
    week_num = 0;
    method = 'new';
    update_item();

}
function featuredEvent() {
    week_num = 0;
    method = 'feature';
    update_item()
}
function allEvent() {
    week_num = 0;
    method = 'index';
    update_item();
}

function realFilter(e) {
    if (e.keyCode === 13) {
        searchInput = document.getElementById("searchBar");
        value = searchInput.value.replace(" ", "-");
        method = 'search';
        week_num = 0;
        update_item();
    }
}

function previous_week() {
    week_num--;
    update_item();

}

function next_week() {
    week_num++;
    update_item();

}

