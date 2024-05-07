$(document).ready(function() {
    var item, title, author, publisher, bookLink, bookImg;
    var outputList = $("#list-output");
    var bookUrl = "https://www.googleapis.com/books/v1/volumes?q=";
    var placeHldr = '<img src="https://via.placeholder.com/150">';
    var searchData;

    $("#search").click(function() {
        outputList.empty(); //empty html output
        searchData = $("#search-box").val();
        //handling empty search input field
        if(searchData === "" || searchData === null) {
            displayError();
        }
        else {
            $.ajax({
                url: bookUrl + searchData,
                dataType: "json",
                success: function(res) {
                    console.log(res)
                    if (res.totalItems === 0) {
                        alert("no result!.. try again")
                    }
                    else {
                        $("#title").animate({'margin-top': '5px'}, 1000); //search box animation
                        $(".book-list").css("visibility", "visible");
                        displayResults(res);
                    }
                },
                error: function () {
                    alert("Something went wrong.. <br>"+"Try again!");
                }
            })
        }
        $("#search-box").val(""); //clear search box
    });

    function displayResults(res) {
        for (var i = 0; i < res.items.length; i+=2){
            item = res.items[i];
            title = item.volumeInfo.title;
            author = item.volumeInfo.authors;
            publisher = item.volumeInfo.publisher;
            bookLink = item.volumeInfo.previewLink;
            bookIsbn = item.volumeInfo.industryIdentifiers[1].identifier;
            bookImg = (item.volumeInfo.imageLinks) ? item.volumeInfo.imageLinks.thumbnail : placeHldr ;
            description = item.volumeInfo.description;
    
            outputList.append(formatOutput(bookImg, title, author, publisher, bookLink, bookIsbn, description));
        }
    }

    function formatOutput(bookImg, title, author, publisher, bookLink, bookIsbn, description) {
        var viewUrl = 'book.html?isbn='+bookIsbn; //constructing link for bookviewer
        var htmlCard = `
            <div class="card" data-book-img="${bookImg}" data-title="${title}" data-author="${author}" data-publisher="${publisher}" data-book-link="${bookLink}" data-book-isbn="${bookIsbn}" data-description="${description}">
                <img src="${bookImg}" class="" alt="...">
                <div class="bottom">
                    <h5 class="title">${title}</h5>
                    <p class="card-text">Author: ${author}</p>
                    <p class="card-text">Publisher: ${publisher}</p>
                    <a target="_blank" href="${viewUrl}" class="amount">Read Book</a>
                </div>
            </div>`;
        return htmlCard;
    }

    // Event delegation to handle click on dynamically generated cards
    $(document).on("click", ".card", function() {
        var cardData = {
            bookImg: $(this).data("book-img"),
            title: $(this).data("title"),
            author: $(this).data("author"),
            publisher: $(this).data("publisher"),
            bookLink: $(this).data("book-link"),
            bookIsbn: $(this).data("book-isbn"),
            description: $(this).data("description")
        };
        displayCardOverlay(cardData);
    });

    // Display error for empty search box
    function displayError() {
        alert("Search term cannot be empty!");
    }

    // Display overlay
    function displayCardOverlay(cardData) {
        var overlayHtml = `
            <div class="overlay">
                <div class="overlay-inner">
                    <button class="close"><i class="fas fa-times"></i></button>
                    <div class="inner-box">
                        <img src="${cardData.bookImg || placeHldr}" alt="" />
                        <div class="info">
                            <h1>${cardData.title}</h1>
                            <h3>${cardData.author}</h3>
                            <h4>${cardData.publisher}<span>${cardData.bookIsbn}</span></h4><br/>
                            <a href="${cardData.bookLink}"><button>More</button></a>
                        </div>
                    </div>
                    <h4 class="description">${cardData.description || ''}</h4>
                </div>
            </div>`;
        $("body").append(overlayHtml);
    }

    // Close overlay
    $(document).on("click", ".close", function() {
        $(".overlay").remove();
    });
});
