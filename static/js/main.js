// Submit post on submit

$(function() {
    // using jQuery
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

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('#comment-form').on('submit', function (event) {
        event.preventDefault();
        create_comment();
        return false;
    });

    // AJAX for posting
    function create_comment() {
        $.ajax({
            url: "/comment", // the endpoint
            type: "POST", // http method
            data: { the_post: $('#form-text').val(), film: $('#film_info').val()}, // data sent with the post request

            // handle a successful response
            success: function (data) {
                console.log(data); // log the returned json to the console
                console.log("success"); // another sanity check
                $('.comments-block').append(
                    "<div class = 'comment'> <div class='comment__info'><span>" + data.author+
                    "</span><span>" + data.created + "</span></div><div>" + data.text  + "</div></div>"
                )

            },

            // handle a non-successful response
            error: function (xhr) {
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }

        });

    }

});