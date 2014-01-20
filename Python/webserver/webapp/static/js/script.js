function sendCommand(kind, group) {
    jQuery.ajax('/api/v1/command/', {
        cache: false,
        data: {
            kind: kind,
            group: group
        },
        mimeType: 'application/json',
        dataType: 'json',
        type: 'post'
    });
}

function csrfSafeMethod(method) {
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

$(function(){
    $.UIPopup({empty: true});
    $('.popup').UIBusy();

    $.ajaxSetup({
        crossDomain: false,
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        }
    });

    $.getJSON('/api/v1/group/', function(response){
        $('.popup').UIPopupClose();
        for (i in response) {
            var group = response[i];
            var element = $('<li class="nav"><h3/><div><a href="javascript:void(null)" class="button on">ON</a><a href="javascript:void(null)" class="button off">OFF</a></div></li>');
            $(element).data('id', group.id);
            $('h3', element).text(group.name);
            $('ul').append(element);
        }
    });

    $(document).on($.eventEnd, '.button.on', function() {
        sendCommand(1, $(this).parent().parent().data('id'));
    });

    $(document).on($.eventEnd, '.button.off', function() {
        sendCommand(2, $(this).parent().parent().data('id'));
    });
});