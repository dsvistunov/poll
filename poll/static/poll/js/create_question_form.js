$(document).ready(function () {

    var inp_cnt = 0;

    $('label[for=id_size]').hide();
    $('#id_size').hide();

    function add_input () {
        inp_cnt += 1;
        var type = $('#id_type').val();
        var remove_btn = '';
        if (type !== 'TXT' && type !== 'NUM' && type !== 'CHK'){
            remove_btn = '<input id="input_remove" type="button" value="-"/>'
        }

        if (type == 'MSL'){
            $('label[for=id_size]').show();
            $('#id_size').show();
        }
        $('#choices').append(
            '<div id="input">' +
            '<label for="input' + inp_cnt + '">Answer text: </label>' +
            '<input type="text" id="input' + inp_cnt + '" name="choice' + inp_cnt + '" placeholder="ansver text">' +
            remove_btn + '</div>'
        )
    }

    $('#form').on('click', '#add_button', function () {
        add_input();
    });

    $('#form').on('click', '#input_remove', function () {
        $(this).closest('#input').remove();
    });

    $('#id_type').change(function () {
        $('#choices').empty();
        $('#add_button').remove();
        $('label[for=id_size]').hide();
        $('#id_size').hide();

        if ($(this).val() == 'NUM'){
            $('#choices').append(
            '<div id="input">' +
            '<label for="input' + inp_cnt + '">Default value: </label>' +
            '<input type="number" id="input' + inp_cnt + '" name="choice' + inp_cnt + '">' +
            'Max value: <input type="number" name="max_value">' +
            'Min value: <input type="number" name="min_value"></div>'
        )}else {
            add_input();
        }

        if ($(this).val() !== 'TXT' && $(this).val() !== 'NUM' && $(this).val() !== 'CHK'){
            $('#button').append('<div id="add_button"><input type="button" value="+"/></div>');
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
                $('#create_button').after(response.msg);
            },
            error: function (xhr) {
                $.each(xhr.responseJSON, function (key, value) {
                    var node = 'input[name=' + key + ']';
                    var message = '<span style="color: red; position: absolute; width: 180px;">' + value + '</span>';
                    $(node).after(message);
                })
            }
        })
    });
});