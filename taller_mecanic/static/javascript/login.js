
$(document).ready(function(){
//Obtenir CSRF_token
let csrf_token = $('[name=csrfmiddlewaretoken]').val();
// Configurar el token CSRF en todas las solicitudes AJAX
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Solo envía el token CSRF si la solicitud no es de origen cruzado
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    }
});


    //Establir focus al input usuari
    $('#usuari').focus();

    //Al realitzar enter sobre els inputs, provocar event
    $('#usuari').keypress(f_executarEnter);
    $('#password').keypress(f_executarEnter);

    
    //Mostrar contrasenya
    $('.show-password').click(function(){
        let passwordField = $(this).prev('input');
        let passwordFieldType = passwordField.attr('type');
        if(passwordFieldType == 'password') {
            passwordField.attr('type', 'text');
            $(this).removeClass('fa-eye-slash').addClass('fa-eye');
        } else {
            passwordField.attr('type', 'password');
            $(this).removeClass('fa-eye').addClass('fa-eye-slash');
        }
    });
});

function f_executarEnter(event) {
    let qt_correcte = 0;
    //KeyCode 13 => Enter
    if (event.keyCode === 13 || event.type==='click') { 
        let usuari = $('#usuari').val().trim();
        let password = $('#password').val().trim();

        // Verificar si els camps són buits
        if (usuari == '') {
            $('#usuari').addClass('error-border'); 
            $('#usuario-error-message').text("L'usuari és obligatori");
            
        } else {
            $('#usuari').removeClass('error-border'); 
            $('#usuario-error-message').text('');
            qt_correcte++;
        }
        
        if (password == '') {
            $('#password').addClass('error-border'); 
            $('#contraseña-error-message').text("La contrasenya és obligatòria");
            return;
        } else {
            $('#password').removeClass('error-border'); 
            $('#contraseña-error-message').text(''); 
            qt_correcte++;
        }

        if(qt_correcte==2){
            //Es correcte, login
            f_login(usuari, password);
        }
    }
}

function f_login(usuari, password){
    

    $.ajax({
        type: 'POST',
        url: '/login/',
        data: {
            'usuari': usuari,
            'password': password
        },
        success: function(data) {
            if (data.success) {
                //Redireccionar
                console.info('SUCCESS');
                window.location.href = data.redirect_url;
            } else {
                Swal.fire({
                    icon: "error",
                    title: "Iniciar sessió",
                    text: "L'usuari o contrasenya no són correctes",
                });
            }
        },
        error: function() {
            Swal.fire({
                icon: "error",
                title: "Iniciar sessió",
                text: "S'ha produït un error a l'intentar iniciar sessió",
            });
        }
    });
}
