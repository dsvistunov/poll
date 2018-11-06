$(document).ready(function () {

    var inp_cnt = 0;

    function add_input (type) {
        inp_cnt += 1;
        var remove_btn = '';
        if (type !== 'text' && type !== 'number'){
            remove_btn = '<input id="input_remove" type="button" value="-"/>'
        }
        $('#choices').append('<div id="input"><label for="input' + inp_cnt + '">Choice text: </label><input type="text" id="input' + inp_cnt + '" name="choice' + inp_cnt + '" placeholder="ansver text">' + remove_btn + '</div>')
    }

    function add_button() {
        $('#button').append('<div id="add_button"><input type="button" value="+"/></div>');
    }

    $('#form').on('click', '#add_button', function () {
        // $('#input').clone().val('').appendTo('#choices').find("input[type='text']").val("");
        add_input();
    });

    $('#form').on('click', '#input_remove', function () {
        $(this).closest('#input').remove();
    });

    $('#types').change(function () {
        $('#choices').empty();
        $('#add_button').remove();
        if ($(this).val() == 'text'){
            add_input('text');
        }else if ($(this).val() == 'radio'){
            add_input('radio');
            add_button();
        }else if ($(this).val() == 'checkbox'){
            add_input('checkbox');
            add_button();
        }else if ($(this).val() == 'select'){
            add_input('select');
            add_button();
        }else if ($(this).val() == 'multiselect'){
            add_input('multiselect');
            add_button();
        }else if ($(this).val() == 'number'){
            add_input('number');
        }
    });

    $('form').submit(function (event) {
        event.preventDefault();
        var form = $(this);

        // from documentation
        // https://docs.djangoproject.com/en/1.11/ref/csrf/#acquiring-the-token-if-csrf-use-sessions-is-false
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        var csrftoken = getCookie('csrftoken');

        // from documentation
        // https://docs.djangoproject.com/en/1.11/ref/csrf/#setting-the-token-on-the-ajax-request
        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        $.ajax({
            method: 'post',
            data: form.serialize(),
            success: function (response) {
                console.log("success");
                console.log(response.msg)
            },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log("errors");
                console.log(xhr.status);
                console.log(thrownError);
                console.log(xhr.responseText)
            }
        })
    });
});