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

$(function() {
	$( "#dialog:ui-dialog" ).dialog( "destroy" );

	var name = $( "#login" ),
        reg_name = $( "#username" ),
        password = $( "#password" ),
		reg_password = $( "#password2" ),
        reg_password2 = $( "#repassword" ),
		email = $( "#email" ),
		allFields = $( [] ).add( name ).add( email ).add( password ),
		tips = $( ".validateTips" );

	function updateTips( t ) {
		tips
			.text( t )
			.addClass( "ui-state-highlight" );
		setTimeout(function() {
			tips.removeClass( "ui-state-highlight", 1500 );
		}, 500 );
	}

	function checkRegexp( o, regexp, n ) {
		if ( !( regexp.test( o.val() ) ) ) {
			o.addClass( "ui-state-error" );
			updateTips( n );
			return false;
		} else {
			return true;
		}
	}

	$( "#dialog-form" ).dialog({
		autoOpen: false,
		height: 330,
		width: 350,
		modal: true,
		buttons: {
			"Вход": function() {
				var bValid = true;
				allFields.removeClass( "ui-state-error" );
                bValid = bValid && checkRegexp( name, /^[a-z]([0-9a-z_])+$/i, "Username may consist of a-z, 0-9, underscores, begin with a letter." );
				bValid = bValid && checkRegexp( password, /^([0-9a-zA-Z])+$/, "Password field only allow : a-z 0-9" );
				if ( bValid ) {
					var pass = document.forms["login_form"].password.value;
					var login = document.forms["login_form"].login.value;
					$.post("/accounts/ajax_login/", { 
                      login: login,
                      password: pass
                    },
                    function(data){
                      if(data == "{{{FAIL}}}")
                        updateTips("Invalid username or password");
                      else{
                        user_is_auth = true;
                        $("#login_buts").hide();
                        $("#user_info").html(data);
    					$("#dialog-form").dialog( "close" );
                      }
                    });
				}
			},
			Отмена: function() {
				$( this ).dialog( "close" );
			}
		},
		close: function() {
			allFields.val( "" ).removeClass( "ui-state-error" );
		}
	});

	$( "#register-form" ).dialog({
		autoOpen: false,
		height: 430,
		width: 350,
		modal: true,
		buttons: {
			"Зарегистрироваться": function() {
				var bValid = true;
                reg_password = $( "#password2" ),
                reg_password2 = $( "#repassword" ),
				allFields.removeClass( "ui-state-error" );
                bValid = bValid && checkRegexp( reg_name, /^[a-z]([0-9a-z_])+$/i, "Username may consist of a-z, 0-9, underscores, begin with a letter." );
				bValid = bValid && checkRegexp( email, /^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i, "eg. ui@jquery.com" );
				bValid = bValid && checkRegexp( reg_password, /^([0-9a-zA-Z])+$/, "Password field only allow : a-z 0-9" );
                bValid = bValid && checkRegexp( reg_password2, /^([0-9a-zA-Z])+$/, "Password field only allow : a-z 0-9" );
                if(bValid)
                if(!(reg_password.val() == reg_password2.val())){
                    updateTips( "Passwords are not equal" );
                    bValid = false;
                }
				if ( bValid ) {
					var pass = document.forms["register_form"].password2.value;
					var username = document.forms["register_form"].username.value;
					var user_email = document.forms["register_form"].email.value;
					$.post("/accounts/ajax_register/", { 
                      username: username,
                      email: user_email,
                      password: pass
                    },
                    function(data){
                      if(data == "{{{USERNAME}}}"){
                        updateTips( "Username is already in use" );
                      }
                      else if(data == "{{{EMAIL}}}"){
                        updateTips( "Email is already in use" );
                      }
                      else{  
                        $("#login_buts").hide();
                        $("#user_info").html(data);
                        $("#register-form").dialog( "close" );
                      }
                    });
				}
			},
			Отмена: function() {
				$( this ).dialog( "close" );
			}
		},
		close: function() {
			allFields.val( "" ).removeClass( "ui-state-error" );
		}
	});

	$( "#login-user" )
		.button()
		.click(function() {
			$( "#dialog-form" ).dialog( "open" );
		});
	$( "#register-user" )
		.button()
		.click(function() {
			$( "#register-form" ).dialog( "open" );
		});
});

/* Ajax logout */ 

function ajax_logout(){
    $.post("/accounts/logout/",
    function(data){
      user_is_auth = false;
      $(".follow_button").hide();
      $("#user_info").html('');
      $("#login_buts").show();
    });
}

