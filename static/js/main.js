// Submit post on submit

$(function () {
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


    $('.comment-form').on('submit', function (event) {
        event.preventDefault();
        create_comment();
        return false;
    });


    $('.f-delete-restore').click(function () {
        var $btn = $(this);

        // AJAX for delete and restore film
        $.ajax({
            url: $btn.data('url'),
            type: 'POST',
            data: {'id': $btn.data('id'), 'flag': $btn.attr('flag')},

            success: function (response) {
                if (response.flag == 1) {
                    $('.f-update').css({"display": "none"});
                    $('.f-delete-restore').html('Восстановить');
                    $('.f-delete-restore').attr("flag", 0);
                    $('.f-restore').css({"display": "block"});

                } else {
                    $('.f-restore').css({"display": "none"});
                    $('.f-update').css({"display": "block"});
                    $('.f-delete-restore').html('Удалить');
                    $('.f-delete-restore').attr("flag", 1);
                }
            }

        });
        return false;

    });

    $('.c-delete-restore').click(function () {
        var $btn = $(this);
        console.log($btn);
        // AJAX for delete and restore film
        $.ajax({
            url: $btn.data('url'),
            type: 'POST',
            data: {'id': $btn.data('id'), 'flag': $btn.attr('flag')},

            success: function (response) {
                if (response.flag == 1) {
                    $btn.html('Восстановить');
                    $btn.attr('flag', 0);
                    console.log("flag is 1");
                    console.log($btn.attr('flag'));
                } else {
                    $btn.html('Скрыть');
                    $btn.attr("flag", 1);
                    console.log("flag is not 1");
                    //$('.f-delete-restore').attr("flag", 1);
                }
            }

        });
        return false;

    });

    $(".f-update").click(function () {
        if ($(".update-film-form").css("display") == 'none') {
            $('.update-film-form').css({"display": "block"});
        } else {
            $('.update-film-form').css({"display": "none"});
        }
    });


    $('.update-film-form').on('submit', function (event) {
        event.preventDefault();
        update_film();
        return false;
    });

    $('.film-score').click(function () {
        var $btn = $(this);

        // AJAX for delete and restore film
        $.ajax({
            url: $btn.data('url'),
            type: 'POST',
            data: {'id': $btn.data('id'), 'mark': $btn.data('mark')},

            success: function (response) {
                alert(response.message);
                $('.film-rating').html(response.rating);
            }
            ,

            // handle a non-successful response
            error: function (xhr) {
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }

        });
        return false;

    });

    // AJAX for posting
    function create_comment() {
        $.ajax({
            url: "/comment", // the endpoint
            type: "POST", // http method
            data: {the_post: $('#form-text').val(), film: $('#film_info').val()}, // data sent with the post request

            // handle a successful response
            success: function (response) {
                console.log(response); // log the returned json to the console
                console.log("success"); // another sanity check
                $('.comments-block').append(
                    "<div class = 'comment'> <div class='comment__info'><span>" + response.author +
                    " </span><span>" + response.created + "</span></div><div>" + response.text + "</div></div>"
                )

            },

            // handle a non-successful response
            error: function (xhr) {
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }

        });

    }


    // AJAX for updating film
    function update_film() {
        $.ajax({
            url: "/update", // the endpoint
            type: "POST", // http method
            data: {
                film: $("input[name$='film-pk']").val(),
                name: $("input[name$='name']").val(),
                year: $("input[name$='year']").val(),
                discription: $("textarea[name$='discription']").val()
            }, // data sent with the post request

            // handle a successful response
            success: function (response) {
                console.log("success"); // sanity check
                $(".film-name").html(response.name);
                $(".film-year").html(response.year);
                $(".film-discription").html(response.discription);
            },

            // handle a non-successful response
            error: function (xhr) {
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }

        });
    }


});


