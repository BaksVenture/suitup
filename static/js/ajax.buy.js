/* Make csrf work with js */
$(document).ajaxSend(function(event, xhr, settings) {
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
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

/* CSRF token */


$(document).ready(function() {    
    $("#dark-background").click(hide_test_cert_popup);
    $("#popup .close").click(hide_test_cert_popup);
});

function buy(item_id){
    $.post("/buy/order", {
        product_id: item_id
    },
    function(data){
        $("#payment_form").html(data);
        $width = (window.innerWidth-$("#popup").width())/2;
        $height = (window.innerHeight-$("#popup").height())/2;
        $("#popup").css({"top": $height, "left": $width}); 
        $("#popup").fadeIn(70);
        $("#dark-background").fadeIn(70);
    });
}

function hide_test_cert_popup(){
    $("#popup").fadeOut(70);
    $("#dark-background").fadeOut(70);
}

function complete_payment(){
    if($("#id_address").val() == "" || $("#id_phone").val() == ""){
        var temp = $("#popup-msg").text();
        $("#popup-msg").html("<font color=\"red\">Fill all fields, please!</font>")
        setTimeout(function() {
			$("#popup-msg").text(temp);
		}, 1000 );
    }
    else{
        document.forms["pay_form"].submit();
    }
}
