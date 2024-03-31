let id_reparacio;
$(document).ready(function() {
    $('.js-example-basic-single').select2();

    //Afegir escoltadors del modal
    $('#f_marca_model').on('change', function() {
        // Lógica que deseas ejecutar cuando cambia el valor seleccionado
        f_comprovarAfegirVehicle();
    });
    document.getElementById('f_matricula').addEventListener('input', f_comprovarAfegirVehicle);
    document.getElementById('f_kms').addEventListener('input', f_comprovarAfegirVehicle);
    $('#f_client').on('change', function() {
        // Lógica que deseas ejecutar cuando cambia el valor seleccionado
        f_comprovarAfegirVehicle();
    });


    document.getElementById('b_guarda_vehicle').addEventListener('click',f_guardaVehicle);
    document.getElementById('b_guarda_reparacio_cap').addEventListener('click',f_guardarReparacionsCapçalera)

});

function f_guardaVehicle(){
    let kms = document.getElementById('f_kms').value;
    let matricula = document.getElementById('f_matricula').value;
    //f_marca_model.val() f_client.val()

    //CRIDA AJAX PER GUARDAR EL VEHICLE
    var csrfToken = $('[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            type: 'POST',
            url: '/add_vehicle/',
            data: {
                'kms': kms,
                'matricula': matricula,
                'marca_model': f_marca_model.val(),
                'client': f_client.val(),
                'csrfmiddlewaretoken': csrfToken,
            },
            success: function(data) {
                if (data.success) {

                    //Tancar modal
                    modal.style.display = "none";
                    //Assignar al select el nou vehicle
                    var nova_opc = new Option(data.vehicle.matricula+" "+data.vehicle.nom, data.vehicle.id, true, true);

                    // Agregamos la nueva opción al select nativo
                    $("#vehicle").append(nova_opc);

                    // Actualizamos el control de Select2
                    $("#vehicle").trigger("change.select2");

                    //Canviem valors dels inputs disableds
                    document.getElementById('marca_model').value = data.vehicle.nom;
                    document.getElementById('kms').value = data.vehicle.kms;
                    document.getElementById('matricula').value = data.vehicle.matricula;
                    
                    Swal.fire({
                        itle: "Guardar vehicle",
                        text: "El vehicle s'ha guardat correctament",
                        icon: "success"
                    });
                    
                } else {
                    Swal.fire({
                        icon: "error",
                        title: "Guardar vehicle",
                        text: "S'ha produït un error guardant el vehicle",
                    });
                }
            },
            error: function() {
                Swal.fire({
                    icon: "error",
                    title: "Guardar vehicle",
                    text: "S'ha produït un error guardant el vehicle",
                });
            }
        });

}

function f_comprovarAfegirVehicle(){
    /*
        Combos amb valor != -1
        Matricula ha de tenir minim 7 caracters (Obl)
        Km ha de ser un numero decimal correcte  (Obl)
    */
    let kms = document.getElementById('f_kms').value;
    let matricula = document.getElementById('f_matricula').value;

    //Validar kms
    const regex = /^\d+(\.\d+)?$/;
    let validar_km = regex.test(kms);
    
    //Validar matricula
    let validar_matricula = (matricula.length >= 7 ? true : false);

    //Validar combos
    let validar_marca_model = (f_marca_model.val() !="-1" ? true : false);
    let validar_client = (f_client.val() !="-1" ? true : false);

    if(validar_km && validar_matricula && validar_client && validar_marca_model){ 
        console.info('Tot ok');
        document.getElementById('b_guarda_vehicle').disabled = false;
    }else{
        console.info('No ok');
        document.getElementById('b_guarda_vehicle').disabled = true;
    }

}

let f_marca_model = $('#f_marca_model');
let f_client = $('#f_client');
var e_vehicle = $('#vehicle');
// Agregar un event listener para el evento change de Select2
e_vehicle.on('select2:select select2:unselect', function (e) {
    // Obtener los elementos seleccionados
    //var selectedOptions = select.val();
    f_emplenarDadesClient(e_vehicle.val());
    
    f_getVehicle(e_vehicle.val());
    
});

var e_client = $('#clients');
e_client.on('select2:select select2:unselect', function (e) {
    // Obtener los elementos seleccionados
    //var selectedOptions = select.val();
    f_emplenarDadesVehicle(e_client.val());
    f_emplenarDadesClient(e_client.val());
    
    
});


function f_guardarReparacionsCapçalera(){
    /*
        Funció que guarda la capçalera de la reparació. Retorna el id de la capçalera que acabem de guardar
        Deshabilita els <select> ya que ja hem guardat la reparació
    */
    console.info('VEHICLE A GUARDAR: '+ e_vehicle.val());
    var csrfToken = $('[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            type: 'POST',
            url: '/add_reparacio/',
            data: {
                'id_vehicle': e_vehicle.val(),
                'csrfmiddlewaretoken': csrfToken,
            },
            success: function(data) {
                if (data.success) {
                    
                    id_reparacio = data.id_reparacio;
                    /*
                    Swal.fire({
                        icon: "success",
                        title: "Guardar reparació",
                        text: "La reparació s'ha guardat correctament, ja pots afegir les feines a realitzar",
                    });
                    */
                    Swal.fire({ 
                        title: "Guardar reparació",
                        text: "La reparació s'ha guardat correctament, ja pots afegir les feines a realitzar",
                        icon: "success"}).then(okay => {
                        if (okay) {           
                            
                            // Redireccionar a la página de detalles de la reparación
                            window.location.href = data.url_reparacio;         
                        }
                    });

                    //No deixar que canvii les dades
                    $('#clients').prop('disabled', true);
                    $('#vehicle').prop('disabled', true);


                        

                } else {
                    Swal.fire({
                        icon: "error",
                        title: "Guardar reparació",
                        text: "S'ha produït un error guardant la reparació",
                    });
                }
            },
            error: function() {
                Swal.fire({
                    icon: "error",
                    title: "Guardar reparació",
                    text: "S'ha produït un error guardant la reparació",
                });
            }
        });

}


function f_getVehicle(id_vehicle){
    if(id_vehicle=="-1"){
        
    }else{
        var csrfToken = $('[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            type: 'POST',
            url: '/get_vehicle/',
            data: {
                'id_vehicle': id_vehicle,
                'csrfmiddlewaretoken': csrfToken,
            },
            success: function(data) {
                if (data.success) {
                    
                    document.getElementById('marca_model').value = data.vehicle.nom;
                    document.getElementById('matricula').value = data.vehicle.matricula;
                    document.getElementById('kms').value = data.vehicle.kms;

                    $('#clients').val(data.vehicle.id_client).trigger('change');

                    document.getElementById('b_guarda_reparacio_cap').disabled = false;
                } else {
                    Swal.fire({
                        icon: "error",
                        title: "Obtenir vehicle",
                        text: "S'ha produït un obtenint les dades del vehicle",
                    });
                }
            },
            error: function() {
                Swal.fire({
                    icon: "error",
                    title: "Obtenir vehicle",
                    text: "S'ha produït un obtenint les dades del vehicle",
                });
            }
        });
    }
}

function f_emplenarDadesVehicle(id_client){
    
    if(id_client=="-1"){
        
    }else{
        console.info('else')
        var csrfToken = $('[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            type: 'POST',
            url: '/get_dades_vehicle/',
            data: {
                'id_client': id_client,
                'csrfmiddlewaretoken': csrfToken,
            },
            success: function(data) {
                if (data.success) {
                    //Retorn de JSON amb dades filtrades
                    console.info(data);
                    let s_vehicles = document.getElementById('vehicle');
                    s_vehicles.innerHTML = "";

                    for(let i=0; i<data.vehicles.length; i++){
                        var opt = document.createElement("option");
                        
                        opt.text = data.vehicles[i].matricula+" "+data.vehicles[i].nom;
                        opt.value = data.vehicles[i].id; // Asignar un valor, si es necesario
                        s_vehicles.add(opt);
                    }
                    document.getElementById('marca_model').value = data.vehicles[0].nom;
                    document.getElementById('matricula').value = data.vehicles[0].matricula;
                    document.getElementById('kms').value = data.vehicles[0].kms;

                    document.getElementById('b_guarda_reparacio_cap').disabled = false;   
                } else {
                    Swal.fire({
                        icon: "error",
                        title: "Obtenir vehicles del client",
                        text: "S'ha produït un obtenint els vehicles del client",
                    });
                }
            },
            error: function() {
                Swal.fire({
                    icon: "error",
                    title: "Obtenir vehicles del client",
                    text: "S'ha produït un obtenint els vehicles del client",
                });
            }
        });
    }
}

function f_emplenarDadesClient(id_vehicle){

    if(id_vehicle=="-1"){
        //Esborrar tots els camps
        document.getElementById('client').value = "";
        document.getElementById('nif').value = "";
        document.getElementById('telf').value = "";
        document.getElementById('email').value = "";
        document.getElementById('direccio').value = "";

        document.getElementById('marca_model').value = "";
        document.getElementById('kms').value = "";
        document.getElementById('matricula').value = "";

        //Mostra el combo dels vehicles ple
        var csrfToken = $('[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            type: 'POST',
            url: '/get_vehicles/',
            data: {
                'csrfmiddlewaretoken': csrfToken,
            },
            success: function(data) {
                if (data.success) {
                    //Retorn de JSON amb dades filtrades
                    
                    let s_vehicles = document.getElementById('vehicle');
                    s_vehicles.innerHTML = "";

                    let json_obj = JSON.parse(data.vehicles);
                    var opt = document.createElement("option");
                    opt.text = "Selecciona...";
                    opt.value = "-1";
                    s_vehicles.add(opt);
                    for(let i=0; i<json_obj.length; i++){
                        var opt = document.createElement("option");

                        opt.text = json_obj[i].matricula+" "+json_obj[i].nom;
                        opt.value = json_obj[i].id;
                        s_vehicles.add(opt);
                    }
                    document.getElementById('b_guarda_reparacio_cap').disabled = true;
                } else {
                    Swal.fire({
                        icon: "error",
                        title: "Obtenir vehicles",
                        text: "S'ha produït un error obtenint les dades dels vehicles",
                    });
                }
            },
            error: function() {
                Swal.fire({
                    icon: "error",
                    title: "Obtenir vehicles",
                    text: "S'ha produït un error obtenint les dades dels vehicles",
                });
            }
        });
        
    }else{
        var csrfToken = $('[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            type: 'POST',
            url: '/get_client/',
            data: {
                'id_vehicle': id_vehicle,
                'csrfmiddlewaretoken': csrfToken,
            },
            success: function(data) {
                if (data.success) {
                    //Retorn de JSON amb dades filtrades
                    console.info(data)
                    document.getElementById('client').value = data.client.nom + " " + data.client.cognoms;
                    document.getElementById('nif').value = data.client.nif;
                    document.getElementById('telf').value = data.client.telefon;
                    document.getElementById('email').value = data.client.email;
                    document.getElementById('direccio').value = data.client.direccio + " - " + data.client.ciutat + " ("+data.client.codi_postal+")"; 
                    //document.getElementById('div_dtl_select').style.display = "flex";
                    
                } else {
                    Swal.fire({
                        icon: "error",
                        title: "Obtenir client",
                        text: "S'ha produït un error obtenint les dades del client",
                    });
                }
            },
            error: function() {
                Swal.fire({
                    icon: "error",
                    title: "Obtenir client",
                    text: "S'ha produït un error obtenint les dades del client",
                });
            }
        });
    }
}

// Obtener el botón y el modal
var btn = document.getElementById("b_add_vehicle");
var modal = document.getElementById("myModal");

// Obtener el span que cierra el modal
var span = document.getElementsByClassName("close")[0];

// Cuando se hace clic en el botón, abrir el modal
btn.onclick = function() {
    modal.style.display = "block";

    //Revisar el valor del combo del client
    //Si té valor, introduir com a seleccionat, en cas contrari, ha d'escollir
    if(e_client.val()!="-1"){
        $('#f_client').val(e_client.val()).trigger('change');
    }
}

// Cuando se hace clic en <span> (x), cerrar el modal
span.onclick = function() {
    modal.style.display = "none";
}

// Cuando se hace clic fuera del modal, cerrar el modal
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}