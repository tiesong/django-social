/**
 * Created by snake on 8/21/2017.
 */
var AllItemsElements;
var searchInput, filter;
var contentChecked, categoryChecked;

// after loading page
$(document).ready(function () {

    // show content by page
    var newsItemsElements = $("#article_list .news-single-item");
    AllItemsElements = newsItemsElements;
    newsPage(newsItemsElements);

    // visible or invisible search box.
    $('#search').click(function () {
        if ($("#search-form").is(':visible')) {
            $("#search-form").fadeOut();
        } else {
            $("#search-form").fadeIn();
        }
    });

    $(document.body).click(function (e) {
        //Hide the search bar if visible
        if (e.target.id !== "searchBar" && e.target.id !== "search" && e.target.id !== "contentCheck" && e.target.id !== "categoryCheck")
            $("#search-form").hide();
    });
});

function handleContent(checkbox) {
    if (checkbox.checked === true) {
        contentChecked = true;
    } else {
        contentChecked = false;
    }
}

function handleCategory(checkbox) {
    if (checkbox.checked === true) {
        categoryChecked = true;
    } else {
        categoryChecked = false;
    }
}

// search keyword in real time.
function realFilter() {
    searchInput = document.getElementById("searchBar");
    filter = searchInput.value.toLowerCase();
    var newsItemsElements = $("#article_list .news-single-item");
    newsItemsElements.hide();

    for (var i = newsItemsElements.length; i--;) {

        var newsItemId = newsItemsElements[i].id;
        var newsItemContentDiv = newsItemsElements[i].children[1];
        var newsItemCategory = newsItemContentDiv.children[0].innerHTML.toLowerCase().split("//")[1].replace(/\s+/g, "");
        var newsItemContent = newsItemContentDiv.children[3].innerHTML.toLowerCase().replace(/\s+/g, "");

        // search tag in category
        if (newsItemCategory.indexOf(filter) > -1) {
            console.log('hide', "#article_" + newsItemId.toString());
        }
        // search tag in news body.
        else if (newsItemContent.indexOf(filter) > -1) {
            console.log('show', "#article_" + newsItemId.toString());
        }

        else {
            console.log('hide', i);
            newsItemsElements.splice(i, 1);

        }
    }
    console.log(newsItemsElements);
    if (newsItemsElements.length !== 0)
        newsPage(newsItemsElements);
}

// paginate contents.
function newsPage(newsItemsElements) {

    var perPage = 5;
    console.log('newsItems ', newsItemsElements);
    newsItemsElements.hide();
    newsItemsElements.slice(0, perPage).show();  // First 5 items show.

    $(".pagination-page").pagination({
        items: newsItemsElements.length,
        itemsOnPage: perPage,
        cssStyle: "light-theme",

        onPageClick: function (pageNumber) {

            var showFrom = perPage * (pageNumber - 1);
            var showTo = showFrom + perPage;

            newsItemsElements.hide().slice(showFrom, showTo).show();
        }
    });

}

function clickAllArticles() {
    AllItemsElements.show();
    newsPage(AllItemsElements);
}

function clickTag(category) {
    console.log("category:", category.toLowerCase());
    var ItemsElements = $("#article_list .news-single-item");
    ItemsElements.hide();

    for (var i = ItemsElements.length; i--;) {
        var ItemContentDiv = ItemsElements[i].children[1];
        var ItemCategory = ItemContentDiv.children[0].innerHTML.split("//")[1].replace(/\s+/g, "");

        if (ItemCategory.toLowerCase() !== category.replace(/\s+/g, "").toLowerCase()) {

            ItemsElements.splice(i, 1);
        }

    }
    console.log(ItemsElements);
    if (ItemsElements.length !== 0)
        newsPage(ItemsElements);

}
