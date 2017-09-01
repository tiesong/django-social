/**
 * Created by snake on 9/1/2017.
 */




// Run once time when loading.....
function Regroup(currentDay, Elements) {

    for (var i = Elements.length; i--;) {
        var itemId = Elements[i].id;
        var a = moment(itemId, 'YYYY-MM-DD');
        var b = moment(currentDay, 'YYYY-MM-DD');
        var sameWeek = b.diff(a, 'week');
        var diffDay = b.diff(a, 'days');
        if (regroupElement.hasOwnProperty(sameWeek)) {
            regroupElement[sameWeek].push(itemId);
        }
        else {
            regroupElement[sameWeek] = [itemId];
        }

        if (Math.abs(diffDay) >= 7)
            Elements.splice(i, 1);

    }
    newElements = Elements;
    AllItemElements = $("#event_items .row-margin-1");
}

// Reality Filter
function realFilter() {
    hideweekNav();
    searchInput = document.getElementById("searchBar");
    filter = searchInput.value.toLowerCase();
    var eventsItemsElements = $("#event_items .row-margin-1");
    eventsItemsElements.hide();

    for (var i = eventsItemsElements.length; i--;) {

        var eventsItemContentDiv = eventsItemsElements[i].children[1].children[0].children[1];
        var eventsItemTitle = eventsItemContentDiv.children[0].innerText.toLowerCase().replace(/\s+/g, "");

        // search tag in event title.
        if (eventsItemTitle.indexOf(filter) > -1) {
            console.log('save');
        }

        else {
            console.log('hide', i);
            eventsItemsElements.splice(i, 1);

        }
    }

    if (eventsItemsElements.length !== 0)
        eventsPage(eventsItemsElements);

}
function showElements() {
    console.log(weekCount);
    if (regroupElement.hasOwnProperty(weekCount)) {
        $("#weekNone").hide();
        for (var i = 0; i < regroupElement[weekCount].length; i++) {
            $("#" + regroupElement[weekCount][i]).show();
        }
    }
    else {
        $("#weekNone").show();
    }
}

function hideElements() {
    console.log(weekCount);
    if (regroupElement.hasOwnProperty(weekCount)) {
        for (var i = 0; i < regroupElement[weekCount].length; i++) {
            $("#" + regroupElement[weekCount][i]).hide();
        }
    }
}

function showweekNav() {
    $("#weekEvent").show();
    $("#allEvent").hide();
}
function hideweekNav() {
    $("#weekEvent").hide();
    $("#allEvent").show();
}

// when click previous week.
function previous_week() {
    console.log('previous_week');
    showweekNav();
    hideElements();
    weekCount++;
    showElements();
}

// when click next week.
function next_week() {
    console.log('next_week');
    showweekNav();
    hideElements();
    weekCount--;
    showElements();
}

// when click new event.
function newEvent() {
    console.log('newEvent');
    hideweekNav();
    hideElements();
    eventsPage(newElements);
}

// when click featuredEvent
function featuredEvent() {
    console.log('featuredEvent');
    hideweekNav();
    hideElements();
}

// when click allEvent
function allEvent() {
    console.log('allEvent');
    hideElements();
    hideweekNav();
    eventsPage(AllItemElements);
}

// paginate contents.
function eventsPage(eventItemsElements) {

    var perPage = 5;
    AllItemElements.hide();
    eventItemsElements.slice(0, perPage).show();  // First 5 items show.

    $(".pagination-page").pagination({
        items: eventItemsElements.length,
        itemsOnPage: perPage,
        cssStyle: "light-theme",

        onPageClick: function (pageNumber) {

            var showFrom = perPage * (pageNumber - 1);
            var showTo = showFrom + perPage;

            eventItemsElements.hide().slice(showFrom, showTo).show();
        }
    });

}

