let id_reparacio;
$(document).ready(function() {
    $('.js-example-basic-single').select2();

    document.getElementById('d_t_feines_reparacio').style.display = "none";

    f_altres_conceptes_escoltadors();
    f_peces_recanvi_escoltadors();
    f_feines_mecanic_escoltadors();

    //Inicialment amagar possibilitat afegir linies a la reparació
    //document.getElementById('div_dtl_select').style.display = "none";

    //Inicialment amagar els divs dels 4 tipus de linies
    document.getElementById('d_ac').style.display = "none";
    document.getElementById('d_p').style.display = "none";
    document.getElementById('d_pr').style.display = "none";
    document.getElementById('d_fm').style.display = "none";

    //Inicialment fins que no introdueixin client i vehicle no es pot afegir linies de reparació
    //document.getElementById('div_dtl_select').style.display = "none";!!!!

    document.getElementById('add_fm').addEventListener('click',f_afegeixFeinesMecanic);
    document.getElementById('add_ac').addEventListener('click',f_afegeixAltresConceptes);
    document.getElementById('add_pr').addEventListener('click',f_afegeixPecesRecanvi);
    document.getElementById('add_p').addEventListener('click', f_afegeixPacks);
});

function f_afegeixAltresConceptes(){
    let id_reparacio = config.reparacio_id;
    console.info('ID-REPARACIO: '+id_reparacio);
    /*
        1.Seleccionar els valors que s'han introduit 
        2.Crida AJAX guardant el valor
        3.Una vegada guardat, crear dinàmicament els valors introduïts(f_generaFeinesMecanic(id_linia_reparacio))
    */

    //1.
    let desc_ac = document.getElementById('desc_ac').value;
    let qt_ac = document.getElementById('qt_ac').value;
    let preu_ac = document.getElementById('preu_ac').value;
    

    //2.
    var csrfToken = $('[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        type: 'POST',
        url: '/add_altres_conceptes/',
        data: {
            'id_reparacio': id_reparacio,
            'desc': desc_ac,
            'qt': qt_ac,
            'preu': preu_ac,
            'csrfmiddlewaretoken': csrfToken,
        },
        success: function(data) {
            if (data.success) {
                
                id_altres_conceptes = data.id_altres_conceptes;

                Swal.fire({
                    icon: "success",
                    title: "Guardar altres conceptes",
                    text: "Altres conceptes s'ha guardat correctament",
                });

                //Generar el codi dinàmicament
                f_generaAltresConceptes(id_altres_conceptes);

            } else {
                Swal.fire({
                    icon: "error",
                    title: "Guardar altres conceptes",
                    text: "S'ha produït un error guardant altres conceptes",
                });
            }
        },
        error: function() {
            Swal.fire({
                icon: "error",
                title: "Guardar altres conceptes",
                text: "S'ha produït un error guardant altres conceptes",
            });
        }
    });
}


function f_afegeixPecesRecanvi(){
    let id_reparacio = config.reparacio_id;
    console.info('ID-REPARACIO: '+id_reparacio);
    /*
        1.Seleccionar els valors que s'han introduit 
        2.Crida AJAX guardant el valor
        3.Una vegada guardat, crear dinàmicament els valors introduïts(f_generaFeinesMecanic(id_linia_reparacio))
    */

    //1.
    let pesa_pr = document.getElementById('pesa_pr').value;
    let codfab_pr = document.getElementById('codfab_pr').value;
    let preu_pr = document.getElementById('preu_pr').value;
    let qt_pr = document.getElementById('qt_pr').value;

    //2.
    var csrfToken = $('[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        type: 'POST',
        url: '/add_pesa_recanvi/',
        data: {
            'id_reparacio': id_reparacio,
            'pesa': pesa_pr,
            'qt': qt_pr,
            'preu': preu_pr,
            'codfab': codfab_pr,
            'csrfmiddlewaretoken': csrfToken,
        },
        success: function(data) {
            if (data.success) {
                
                id_pesa_recanvi = data.id_pesa_recanvi;

                Swal.fire({
                    icon: "success",
                    title: "Guardar peça recanvi",
                    text: "La peça de recanvi s'ha guardat correctament",
                });

                //Generar el codi dinàmicament
                f_generaPecesRecanvi(id_pesa_recanvi);

            } else {
                Swal.fire({
                    icon: "error",
                    title: "Guardar peça recanvi",
                    text: "S'ha produït un error guardant la peça de recanvi",
                });
            }
        },
        error: function() {
            Swal.fire({
                icon: "error",
                title: "Guardar feina mecànic",
                text: "S'ha produït un error guardant la feina del mecànic",
            });
        }
    });
}

function f_afegeixPacks(){
    let id_reparacio = config.reparacio_id;
    console.info('ID-REPARACIO: '+id_reparacio);
    /*
        1.Seleccionar els valors que s'han introduit 
        2.Crida AJAX guardant el valor
        3.Una vegada guardat, crear dinàmicament els valors introduïts(f_generaFeinesMecanic(id_linia_reparacio))
    */

    //1.
    let pack_valor = $('#packs').val();
    let pack_desc = $('#packs option:selected').text();
    let pack_preu = document.getElementById('preu_p').value;
    

    //2.
    var csrfToken = $('[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        type: 'POST',
        url: '/add_packs/',
        data: {
            'id_reparacio': id_reparacio,
            'id_pack': pack_valor,
            'preu': pack_preu,
            'desc': pack_desc,
            'csrfmiddlewaretoken': csrfToken,
        },
        success: function(data) {
            if (data.success) {
                
                id_pack = data.id_pack;

                Swal.fire({
                    icon: "success",
                    title: "Guardar pack",
                    text: "El pack s'ha guardat correctament",
                });

                //Generar el codi dinàmicament
                f_generaPacks(id_pack);

            } else {
                Swal.fire({
                    icon: "error",
                    title: "Guardar pack",
                    text: "S'ha produït un error guardant el pack",
                });
            }
        },
        error: function() {
            Swal.fire({
                icon: "error",
                title: "Guardar pack",
                text: "S'ha produït un error guardant el pack",
            });
        }
    });
}

function f_afegeixFeinesMecanic(){
    let id_reparacio = config.reparacio_id;
    console.info('ID-REPARACIO: '+id_reparacio);
    /*
        1.Seleccionar els valors que s'han introduit 
        2.Crida AJAX guardant el valor
        3.Una vegada guardat, crear dinàmicament els valors introduïts(f_generaFeinesMecanic(id_linia_reparacio))
    */

    //1.
    let desc_fm = document.getElementById('desc_fm').value;
    let qt_fm = document.getElementById('qt_fm').value;
    let preu_fm = document.getElementById('preu_fm').value;

    //2.
    var csrfToken = $('[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        type: 'POST',
        url: '/add_feina_mecanic/',
        data: {
            'id_reparacio': id_reparacio,
            'desc': desc_fm,
            'qt': qt_fm,
            'preu': preu_fm,
            'csrfmiddlewaretoken': csrfToken,
        },
        success: function(data) {
            if (data.success) {
                
                id_linia_reparacio = data.id_linia_reparacio;

                Swal.fire({
                    icon: "success",
                    title: "Guardar feina mecànic",
                    text: "La feina del mecànic s'ha guardat correctament",
                });

                //Generar el codi dinàmicament
                f_generaFeinesMecanic(id_linia_reparacio);

            } else {
                Swal.fire({
                    icon: "error",
                    title: "Guardar feina mecànic",
                    text: "S'ha produït un error guardant la feina del mecànic",
                });
            }
        },
        error: function() {
            Swal.fire({
                icon: "error",
                title: "Guardar feina mecànic",
                text: "S'ha produït un error guardant la feina del mecànic",
            });
        }
    });


}

function f_guardaCanvisPecesRecanvi(id_linia_reparacio){
    

    let id_reparacio = config.reparacio_id;

    let pesa_pr = document.getElementById(id_linia_reparacio+'-pesa_pr').value;
    let codfab_pr = document.getElementById(id_linia_reparacio+'-codfab_pr').value;
    let preu_pr = document.getElementById(id_linia_reparacio+'-preu_pr').value;
    let qt_pr = document.getElementById(id_linia_reparacio+'-qt_pr').value;

    const valida_preu = /^\d+(\.\d+)?$/;
    const valida_qt = /^\d+(\.(25|5|75|0))?$/;
    let b_valida_preu = true;
    let b_valida_qt = true;

    if(preu_pr.length!=0){
        b_valida_preu = valida_preu.test(preu_pr);
    }
    if(qt_pr.length!=0){
        b_valida_qt = valida_qt.test(qt_pr);
    }


    if(pesa_pr.length>0 && codfab_pr.length>0 && b_valida_preu && b_valida_qt){
        var csrfToken = $('[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            type: 'POST',
            url: '/editar_pesa_recanvi/',
            data: {
                'id_reparacio': id_reparacio,
                'id_linia_reparacio': id_linia_reparacio,
                'codfab': codfab_pr,
                'pesa': pesa_pr,
                'qt': qt_pr,
                'preu': preu_pr,
                'csrfmiddlewaretoken': csrfToken,
            },
            success: function(data) {
                if (data.success) {
                    Swal.fire({
                        icon: "success",
                        title: "Guardar canvis peça recanvi",
                        text: "Els canvis s'han guardat correctament",
                    });

                } else {
                    Swal.fire({
                        icon: "error",
                        title: "Guardar canvis peça recanvi",
                        text: "S'ha produït un error guardant els canvis de peça recanvi",
                    });
                }
            },
            error: function() {
                Swal.fire({
                    icon: "error",
                    title: "Guardar canvis peça recanvi",
                    text: "S'ha produït un error guardant els canvis de peça recanvi",
                });
            }
        });
    }else{
        Swal.fire({
            icon: "error",
            title: "Guardar canvis peça recanvi",
            text: "S'ha produït un error de validació dels camps a modificar. La peça i el codi de fabricant són camps obligatori. El preu ha de ser un número vàlid",
        });
    }
}


function f_guardaCanvisAltresConceptes(id_linia_reparacio){
    let id_reparacio = config.reparacio_id;

    let desc_ac = document.getElementById(id_linia_reparacio+'-desc_ac').value;
    let preu_ac = document.getElementById(id_linia_reparacio+'-preu_ac').value;
    let qt_ac = document.getElementById(id_linia_reparacio+'-qt_ac').value;
    const valida_preu = /^\d+(\.\d+)?$/;
    const valida_qt = /^\d+(\.(25|5|75|0))?$/;
    let b_valida_preu = true;
    let b_valida_qt = true;

    if(preu_pr.length!=0){
        b_valida_preu = valida_preu.test(preu_ac);
    }
    if(qt_pr.length!=0){
        b_valida_qt = valida_qt.test(qt_ac);
    }


    if(desc_ac.length>0 && b_valida_preu && b_valida_qt){
        var csrfToken = $('[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            type: 'POST',
            url: '/editar_altres_conceptes/',
            data: {
                'id_reparacio': id_reparacio,
                'id_linia_reparacio': id_linia_reparacio,
                'desc': desc_ac,
                'qt': qt_ac,
                'preu': preu_ac,
                'csrfmiddlewaretoken': csrfToken,
            },
            success: function(data) {
                if (data.success) {
                    Swal.fire({
                        icon: "success",
                        title: "Guardar canvis altres conceptes",
                        text: "Els canvis s'han guardat correctament",
                    });

                } else {
                    Swal.fire({
                        icon: "error",
                        title: "Guardar canvis altres conceptes",
                        text: "S'ha produït un error guardant els canvis d'altres conceptes",
                    });
                }
            },
            error: function() {
                Swal.fire({
                    icon: "error",
                    title: "Guardar canvis altres conceptes",
                    text: "S'ha produït un error guardant els canvis d'altres conceptes",
                });
            }
        });
    }else{
        Swal.fire({
            icon: "error",
            title: "Guardar canvis altres conceptes",
            text: "S'ha produït un error de validació dels camps a modificar. La descripció és obligatòria. El preu ha de ser un número vàlid",
        });
    }

}

function f_guardaCanvisPacks(id_linia_reparacio){
    let id_reparacio = config.reparacio_id;

    let id_pack = $('#'+id_linia_reparacio+'-packs').val();
    let desc_pack = $('#'+id_linia_reparacio+'-packs option:selected').text();
    let preu_pack = document.getElementById(id_linia_reparacio+'-preu_p').value;

    var csrfToken = $('[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        type: 'POST',
        url: '/editar_packs/',
        data: {
            'id_reparacio': id_reparacio,
            'id_linia_reparacio': id_linia_reparacio,
            'desc': desc_pack,
            'id_pack': id_pack,
            'preu': preu_pack,
            'csrfmiddlewaretoken': csrfToken,
        },
        success: function(data) {
            if (data.success) {
                Swal.fire({
                    icon: "success",
                    title: "Guardar canvis packs",
                    text: "Els canvis s'han guardat correctament",
                });

            } else {
                Swal.fire({
                    icon: "error",
                    title: "Guardar canvis packs",
                    text: "S'ha produït un error guardant els canvis del pack",
                });
            }
        },
        error: function() {
            Swal.fire({
                icon: "error",
                title: "Guardar canvis packs",
                text: "S'ha produït un error guardant els canvis del pack",
            });
        }
    });
    
}

$(document).on('change', '.js-example-basic-single', function() {
    // Obtiene el valor seleccionado
    var selectedValue = $(this).val();
    // Obtiene el texto seleccionado
    var selectedText = $(this).find('option:selected').text();
    var selectId = $(this).attr('id');
    

    var indiceGuion = selectId.indexOf('-');

    let s_f;
    // Verifica si se encontró un guion
    if (indiceGuion !== -1) {
        // Retorna la subcadena desde el inicio hasta la posición del guion
        s_f = selectId.substring(0, indiceGuion);
    }

    if(selectId!="definicio_tipus_linia" && selectId!="packs"){
        var packs_json = JSON.parse(config.packs_json);
        for(let i=0; i<packs_json.length; i++){
            if(selectedValue == packs_json[i].id){
                console.info("proceder: "+s_f+'-preu_p');
                document.getElementById(s_f+'-preu_p').value = packs_json[i].preu;
                break;
            }
        }
    }
    
    
    

    // Aquí puedes realizar las acciones que deseas con el valor y el texto seleccionado
    console.log('Valor seleccionado:', selectedValue);
    console.log('Texto seleccionado:', selectedText);
});


function f_generaPacks(id_p) {
    // Div principal
    var divPrincipal = document.createElement('div');
    divPrincipal.classList.add('titled-border', 'feines_mecanic');
    divPrincipal.id = id_p + '-d_p';

    // Container del título
    var divTitleContainer = document.createElement('div');
    divTitleContainer.classList.add('title-container');
    var divTitle = document.createElement('div');
    divTitle.classList.add('title');
    divTitle.textContent = 'Packs';
    divTitleContainer.appendChild(divTitle);
    divPrincipal.appendChild(divTitleContainer);

    // Container
    var divContainer = document.createElement('div');
    divContainer.classList.add('container');
    divContainer.style.marginTop = '10px';
    var divRow = document.createElement('div');
    divRow.classList.add('row');

    // Elementos del formulario
    var elementos = [
        { label: 'Pack:', id: id_p + '-packs', col: 'col-lg-5 col-xs-5', select: true },
        { label: 'Preu:', id: id_p + '-preu_p', col: 'col-lg-2 col-xs-2', input: true, disabled: true }
    ];
    
    let preu_pack;
    elementos.forEach(function(elemento) {
        var divCol = document.createElement('div');
        divCol.classList.add('col-lg-1', 'col-xs-1');
        var label = document.createElement('label');
        label.innerHTML = (elemento.label.includes('text-danger')) ? elemento.label : elemento.label + '<span class="text-danger">*</span>';
        divCol.appendChild(label);

        var divInputCol = document.createElement('div');
        divInputCol.className = elemento.col;

        if (elemento.select) {
            var select = document.createElement('select');
            select.classList.add('js-example-basic-single');
            select.id = elemento.id;
            select.style.width = '320px';

            
            var packs_json = JSON.parse(config.packs_json);
            console.info(packs_json);

            for(let i=0; i<packs_json.length; i++){
                let option = document.createElement("option");
                option.value = packs_json[i].id;
                option.textContent = packs_json[i].nom;
                select.appendChild(option);
            }
        
            divInputCol.appendChild(select);
            $(select).select2();
            $(select).val($('#packs').val()).trigger('change');
                
        }

        if (elemento.input) {
            var input = document.createElement('input');
            input.type = 'text';
            input.classList.add('form-control', 'mb-2');
            input.id = elemento.id;
            input.value = document.getElementById('preu_p').value;
            if (elemento.disabled) {
                input.disabled = true;
            }
            divInputCol.appendChild(input);
        }

        divRow.appendChild(divCol);
        divRow.appendChild(divInputCol);
    });

    //Buttons
    var botones = [
        { id: id_p + '-guarda_canvis', onclick: 'f_guardaCanvisPacks(' + id_p + ')', icono: 'fa-floppy-disk', param: id_p },
        { id: id_p + '-elimina_feina', onclick: 'f_eliminaTipusFeina(' + id_p + ')', icono: 'fa-trash', param: id_p }
    ];

    botones.forEach(function(boton) {
        var divCol = document.createElement('div');
        if(boton.icono=='fa-floppy-disk'){
            divCol.classList.add('col-lg-11', 'col-xs-11');
        }else{
            divCol.classList.add('col-lg-1', 'col-xs-1');
        }
        
        var button = document.createElement('button');
        button.classList.add('b_elimina_filtre');
        button.title = (boton.id.includes('guarda_canvis')) ? 'Guardar canvis' : 'Eliminar feina';
        button.id = boton.id;

        //Escoltadors dels buttons
        button.addEventListener('click', function() {
            if (boton.id.includes('guarda_canvis')) {
                f_guardaCanvisPacks(boton.param);
            } else {
                f_eliminaTipusFeina(boton.param);
            }
        });

        var icon = document.createElement('i');
        icon.classList.add('fa-solid', boton.icono, 'fa-xl');
        button.appendChild(icon);
        divCol.appendChild(button);
        divRow.appendChild(divCol);
    });
    divContainer.appendChild(divRow);
    divPrincipal.appendChild(divContainer);

    var d_feines_reparacio = document.getElementById("feines_reparacio");
    d_feines_reparacio.appendChild(divPrincipal);



}

function f_generaAltresConceptes(id_ac) {
    // Div principal
    var divPrincipal = document.createElement('div');
    divPrincipal.classList.add('titled-border', 'feines_mecanic');
    divPrincipal.id = id_ac + '-d_ac';

    // Container del titol
    var divTitleContainer = document.createElement('div');
    divTitleContainer.classList.add('title-container');
    var divTitle = document.createElement('div');
    divTitle.classList.add('title');
    divTitle.textContent = 'Altres conceptes';
    divTitleContainer.appendChild(divTitle);
    divPrincipal.appendChild(divTitleContainer);

    // Container
    var divContainer = document.createElement('div');
    divContainer.classList.add('container');
    divContainer.style.marginTop = '10px';
    var divRow = document.createElement('div');
    divRow.classList.add('row');

    // Elements del formulari
    var elementos = [
        { label: 'Descripció:', id: id_ac + '-desc_ac', col: 'col-lg-4 col-xs-4', valor: document.getElementById('desc_ac').value },
        { label: 'Quantitat:', id: id_ac + '-qt_ac', col: 'col-lg-1 col-xs-1', valor: '1', errorId: 'ac_qt_error', valor: document.getElementById('qt_ac').value },
        { label: 'Preu:', id: id_ac + '-preu_ac', col: 'col-lg-2 col-xs-2', errorId: id_ac + '-ac_preu_error', valor: document.getElementById('preu_ac').value }
    ];

    elementos.forEach(function(elemento) {
        var divCol = document.createElement('div');
        divCol.classList.add('col-lg-1', 'col-xs-1');
        var label = document.createElement('label');
        label.innerHTML = (elemento.label.includes('text-danger')) ? elemento.label : elemento.label + '<span class="text-danger">*</span>';
        divCol.appendChild(label);

        var divInputCol = document.createElement('div');
        divInputCol.className = elemento.col;
        var input = document.createElement('input');
        input.type = 'text';
        input.classList.add('form-control', 'mb-2');
        input.id = elemento.id;
        if (elemento.valor) {
            input.value = elemento.valor;
        }

        input.addEventListener('input', function() {
            console.log('Id: ' + elemento.id + " Error: id: " + elemento.errorId);
        });

        divInputCol.appendChild(input);
        divRow.appendChild(divCol);
        divRow.appendChild(divInputCol);
    });

    //Buttons
    var botones = [
        { id: id_ac + '-guarda_canvis', onclick: 'f_guardaCanvisPecesRecanvi(' + id_ac + ')', icono: 'fa-floppy-disk', param: id_ac },
        { id: id_ac + '-elimina_feina', onclick: 'f_eliminaTipusFeina(' + id_ac + ')', icono: 'fa-trash', param: id_ac }
    ];

    botones.forEach(function(boton) {
        var divCol = document.createElement('div');
        if(boton.icono=='fa-floppy-disk'){
            divCol.classList.add('col-lg-11', 'col-xs-11');
        }else{
            divCol.classList.add('col-lg-1', 'col-xs-1');
        }
        
        var button = document.createElement('button');
        button.classList.add('b_elimina_filtre');
        button.title = (boton.id.includes('guarda_canvis')) ? 'Guardar canvis' : 'Eliminar feina';
        button.id = boton.id;

        //Escoltadors dels buttons
        button.addEventListener('click', function() {
            if (boton.id.includes('guarda_canvis')) {
                f_guardaCanvisAltresConceptes(boton.param);
            } else {
                f_eliminaTipusFeina(boton.param);
            }
        });

        var icon = document.createElement('i');
        icon.classList.add('fa-solid', boton.icono, 'fa-xl');
        button.appendChild(icon);
        divCol.appendChild(button);
        divRow.appendChild(divCol);
    });
    divContainer.appendChild(divRow);
    divPrincipal.appendChild(divContainer);

    var d_feines_reparacio = document.getElementById("feines_reparacio");
    d_feines_reparacio.appendChild(divPrincipal);

    //Netejar camps de text
    document.getElementById('desc_ac').value = "";
    document.getElementById('qt_ac').value = "1";
    document.getElementById('preu_ac').value = "";
}

function f_generaPecesRecanvi(id_pesa_recanvi){
    // Div principal
    var divPrincipal = document.createElement('div');
    divPrincipal.classList.add('titled-border', 'feines_mecanic');
    divPrincipal.id = id_pesa_recanvi+'-d_pr';

    // Container del titol
    var divTitleContainer = document.createElement('div');
    divTitleContainer.classList.add('title-container');
    var divTitle = document.createElement('div');
    divTitle.classList.add('title');
    divTitle.textContent = 'Peces recanvi';
    divTitleContainer.appendChild(divTitle);
    divPrincipal.appendChild(divTitleContainer);

    // Container
    var divContainer = document.createElement('div');
    divContainer.classList.add('container');
    divContainer.style.marginTop = '10px';
    var divRow = document.createElement('div');
    divRow.classList.add('row');

    //Elements del formulari
    var elementos = [
        { label: 'Peça:', id: id_pesa_recanvi+'-pesa_pr', col: 'col-lg-4 col-xs-4', valor: document.getElementById('pesa_pr').value },
        { label: 'Codi fabricant:', id: id_pesa_recanvi+'-codfab_pr', col: 'col-lg-3 col-xs-3', valor: document.getElementById('codfab_pr').value },
        { label: 'Quantitat:', id: id_pesa_recanvi+'-qt_pr', col: 'col-lg-2 col-xs-2', valor: '1', errorId: 'pr_qt_error', valor: document.getElementById('qt_pr').value },
        { label: 'Preu:', id: id_pesa_recanvi+'-preu_pr', col: 'col-lg-2 col-xs-2', errorId: id_pesa_recanvi+'-pr_preu_error', valor: document.getElementById('preu_pr').value }
    ];

    elementos.forEach(function(elemento) {
        var divCol = document.createElement('div');
        divCol.classList.add('col-lg-1', 'col-xs-1');
        var label = document.createElement('label');
        label.innerHTML = (elemento.label.includes('text-danger')) ? elemento.label : elemento.label + '<span class="text-danger">*</span>';
        divCol.appendChild(label);

        var divInputCol = document.createElement('div');
        divInputCol.className = elemento.col;
        var input = document.createElement('input');
        input.type = 'text';
        input.classList.add('form-control', 'mb-2');
        input.id = elemento.id;
        if (elemento.valor) {
            input.value = elemento.valor;
        }

        input.addEventListener('input', function() {
            console.log('Id: ' + elemento.id + " Error: id: " + elemento.errorId);
        });

        divInputCol.appendChild(input);
        divRow.appendChild(divCol);
        divRow.appendChild(divInputCol);
    });

    //Buttons
    var botones = [
        { id: id_pesa_recanvi + '-guarda_canvis', onclick: 'f_guardaCanvisPecesRecanvi(' + id_pesa_recanvi + ')', icono: 'fa-floppy-disk', param: id_pesa_recanvi },
        { id: id_pesa_recanvi + '-elimina_feina', onclick: 'f_eliminaTipusFeina(' + id_pesa_recanvi + ')', icono: 'fa-trash', param: id_pesa_recanvi }
    ];

    botones.forEach(function(boton) {
        var divCol = document.createElement('div');
        if(boton.icono=='fa-floppy-disk'){
            divCol.classList.add('col-lg-8', 'col-xs-8');
        }else{
            divCol.classList.add('col-lg-1', 'col-xs-1');
        }
        
        var button = document.createElement('button');
        button.classList.add('b_elimina_filtre');
        button.title = (boton.id.includes('guarda_canvis')) ? 'Guardar canvis' : 'Eliminar feina';
        button.id = boton.id;

        //Escoltadors dels buttons
        button.addEventListener('click', function() {
            if (boton.id.includes('guarda_canvis')) {
                f_guardaCanvisPecesRecanvi(boton.param);
            } else {
                f_eliminaTipusFeina(boton.param);
            }
        });

        var icon = document.createElement('i');
        icon.classList.add('fa-solid', boton.icono, 'fa-xl');
        button.appendChild(icon);
        divCol.appendChild(button);
        divRow.appendChild(divCol);
    });
    divContainer.appendChild(divRow);
    divPrincipal.appendChild(divContainer);

    var d_feines_reparacio = document.getElementById("feines_reparacio");
    d_feines_reparacio.appendChild(divPrincipal);

    //Netejar camps de text
    document.getElementById('pesa_pr').value = "";
    document.getElementById('codfab_pr').value = "";
    document.getElementById('qt_pr').value = "1";
    document.getElementById('preu_pr').value = "";
}

function f_generaFeinesMecanic(id_linia_reparacio) {
    // Div principal
    var divPrincipal = document.createElement('div');
    divPrincipal.classList.add('titled-border', 'feines_mecanic');
    divPrincipal.id = id_linia_reparacio + '-d_fm';

    // Container del titol
    var divTitleContainer = document.createElement('div');
    divTitleContainer.classList.add('title-container');
    var divTitle = document.createElement('div');
    divTitle.classList.add('title');
    divTitle.textContent = 'Feines mecànic';
    divTitleContainer.appendChild(divTitle);
    divPrincipal.appendChild(divTitleContainer);

    // Container
    var divContainer = document.createElement('div');
    divContainer.classList.add('container');
    var divRow = document.createElement('div');
    divRow.classList.add('row');

    //Elements del formulari
    var elementos = [
        { label: 'Descripció:', id: id_linia_reparacio + '-desc_fm', col: 'col-lg-4 col-xs-4 ml-3', tipo: 'text', valor: document.getElementById('desc_fm').value },
        { label: 'Quantitat:', id: id_linia_reparacio + '-qt_fm', col: 'col-lg-1 col-xs-1', tipo: 'text', valor: document.getElementById('qt_fm').value, errorId: id_linia_reparacio + '-fm_qt_error' },
        { label: 'Preu:', id: id_linia_reparacio + '-preu_fm', col: 'col-lg-2 col-xs-2', tipo: 'text', errorId: id_linia_reparacio + '-fm_preu_error', valor: document.getElementById('preu_fm').value }
    ];

    elementos.forEach(function(elemento) {
        var divCol = document.createElement('div');
        divCol.classList.add('col-lg-1', 'col-xs-1');
        divCol.style = "margin-right: 20px;";

        var label = document.createElement('label');
        label.textContent = elemento.label;
        divCol.appendChild(label);

        var divInputCol = document.createElement('div');
        divInputCol.className = elemento.col.replace(/\s+/g, ''); 
        var input = document.createElement('input');
        input.type = elemento.tipo;
        input.classList.add('form-control', 'mb-2');
        input.id = elemento.id;
        if (elemento.valor) {
            input.value = elemento.valor;
        }

        input.addEventListener('input', function() {
            
            
            console.log('Id: '+ elemento.id+" Error: id: "+elemento.errorId);
        });

        divInputCol.appendChild(input);
        divRow.appendChild(divCol);
        divRow.appendChild(divInputCol);
    });

    //Buttons
    var botones = [
        { id: id_linia_reparacio + '-guarda_canvis', onclick: 'f_guardaCanvis(' + id_linia_reparacio + ')', icono: 'fa-floppy-disk', param: id_linia_reparacio },
        { id: id_linia_reparacio + '-elimina_feina', onclick: 'f_eliminaTipusFeina(' + id_linia_reparacio + ')', icono: 'fa-trash', param: id_linia_reparacio }
    ];

    botones.forEach(function(boton) {
        var divCol = document.createElement('div');
        divCol.classList.add('col-lg-1', 'col-xs-1');
        var button = document.createElement('button');
        button.classList.add('b_elimina_filtre');
        button.title = (boton.id.includes('guarda_canvis')) ? 'Guardar canvis' : 'Eliminar feina';
        button.id = boton.id;

        //Escoltadors dels buttons
        button.addEventListener('click', function() {
            if (boton.id.includes('guarda_canvis')) {
                f_guardaCanvis(boton.param);
            } else {
                f_eliminaTipusFeina(boton.param);
            }
        });

        var icon = document.createElement('i');
        icon.classList.add('fa-solid', boton.icono, 'fa-xl');
        button.appendChild(icon);
        divCol.appendChild(button);
        divRow.appendChild(divCol);
    });


    divContainer.appendChild(divRow);
    divPrincipal.appendChild(divContainer);

    var d_feines_reparacio = document.getElementById("feines_reparacio");
    d_feines_reparacio.appendChild(divPrincipal);

    //Netejar camps de text
    document.getElementById('desc_fm').value = "";
    document.getElementById('qt_fm').value = "1";
    document.getElementById('preu_fm').value = "";
}

    

function f_guardaCanvis(id_linia_reparacio){
    
    let id_reparacio = config.reparacio_id;

    let desc = document.getElementById(id_linia_reparacio+'-desc_fm').value;
    let qt = document.getElementById(id_linia_reparacio+'-qt_fm').value;
    let preu = document.getElementById(id_linia_reparacio+'-preu_fm').value;

    const valida_preu = /^\d+(\.\d+)?$/;
    const valida_qt = /^\d+(\.(25|5|75|0))?$/;
    let b_valida_preu = true;
    let b_valida_qt = true;

    if(preu.length!=0){
        b_valida_preu = valida_preu.test(preu);
    }
    if(qt.length!=0){
        b_valida_qt = valida_qt.test(qt);
    }


    if(desc.length>0 && b_valida_preu && b_valida_qt){
        var csrfToken = $('[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            type: 'POST',
            url: '/editar_feina_mecanic/',
            data: {
                'id_reparacio': id_reparacio,
                'id_linia_reparacio': id_linia_reparacio,
                'desc': desc,
                'qt': qt,
                'preu': preu,
                'csrfmiddlewaretoken': csrfToken,
            },
            success: function(data) {
                if (data.success) {
                    Swal.fire({
                        icon: "success",
                        title: "Guardar canvis feina mecànic",
                        text: "Els canvis s'han guardat correctament",
                    });

                } else {
                    Swal.fire({
                        icon: "error",
                        title: "Guardar canvis feina mecànic",
                        text: "S'ha produït un error guardant els canvis de feina mecànic",
                    });
                }
            },
            error: function() {
                Swal.fire({
                    icon: "error",
                    title: "Guardar canvis feina mecànic",
                    text: "S'ha produït un error guardant els canvis de feina mecànic",
                });
            }
        });
    }else{
        Swal.fire({
            icon: "error",
            title: "Guardar canvis feina mecànic",
            text: "S'ha produït un error de validació dels camps a modificar. La descripció és un camp obligatori. El preu ha de ser un número vàlid",
        });
    }

    


}

function f_eliminaTipusFeina(id_linia_reparacio){
    Swal.fire({
        title: "Estàs segur que vols eliminar-lo?",
        //text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Elimina"
        }).then((result) => {
        if (result.isConfirmed) {  
            let id_reparacio = config.reparacio_id;

            var csrfToken = $('[name="csrfmiddlewaretoken"]').val();
            $.ajax({
                type: 'POST',
                url: '/eliminar_feina_mecanic/',
                data: {
                    'id_linia_reparacio': id_linia_reparacio,
                    'csrfmiddlewaretoken': csrfToken,
                },
                success: function(data) {
                    if (data.success) {
                        try{
                            document.getElementById(id_linia_reparacio+'-d_fm').innerHTML = "";
                            document.getElementById(id_linia_reparacio+'-d_fm').style.display = "none";
                        }catch(e){};

                        try{
                            document.getElementById(id_linia_reparacio+'-d_pr').innerHTML = "";
                            document.getElementById(id_linia_reparacio+'-d_pr').style.display = "none";
                        }catch(e){};

                        try{
                            document.getElementById(id_linia_reparacio+'-d_ac').innerHTML = "";
                            document.getElementById(id_linia_reparacio+'-d_ac').style.display = "none";
                        }catch(e){};

                        try{
                            document.getElementById(id_linia_reparacio+'-d_p').innerHTML = "";
                            document.getElementById(id_linia_reparacio+'-d_p').style.display = "none";
                        }catch(e){};
                        
    
                        Swal.fire({
                            icon: "success",
                            title: "Eliminar feina",
                            text: "La feina s'ha eliminat correctament",
                        });
    
                    } else {
                        Swal.fire({
                            icon: "error",
                            title: "Eliminar feina",
                            text: "S'ha produït un error a intentar eliminar la feina",
                        });
                    }
                },
                error: function() {
                    Swal.fire({
                        icon: "error",
                        title: "Eliminar feina",
                        text: "S'ha produït un error a intentar eliminar la feina",
                    });
                }
            });
        }
        });


    
}



function f_feines_mecanic_escoltadors(){
    //Afegir escoltadors
    document.getElementById('desc_fm').addEventListener('input', f_comprovarFeinesMecanic);
    document.getElementById('qt_fm').addEventListener('input', f_comprovarFeinesMecanic);
    document.getElementById('preu_fm').addEventListener('input', f_comprovarFeinesMecanic);
}

function f_comprovarFeinesMecanic(){
    let desc = document.getElementById('desc_fm').value;
    let qt = document.getElementById('qt_fm').value;
    let preu = document.getElementById('preu_fm').value;

    if(desc.length==0){
        document.getElementById('add_fm').disabled = true;
        f_validarPreu(preu,"fm_preu_error");
        f_validarQuantitats(qt,"fm_qt_error");

    }else{    
        document.getElementById('add_fm').disabled = f_validarPreu(preu,"fm_preu_error") || f_validarQuantitats(qt,"fm_qt_error") || (desc.length > 0 ? false : true);
    }
}

function f_altres_conceptes_escoltadors(){
    //Afegir escoltadors
    document.getElementById('desc_ac').addEventListener('input', f_comprovaAltresConceptes);
    document.getElementById('qt_ac').addEventListener('input', f_comprovaAltresConceptes);
    document.getElementById('preu_ac').addEventListener('input', f_comprovaAltresConceptes);
}

function f_peces_recanvi_escoltadors(){
    document.getElementById('pesa_pr').addEventListener('input',f_comprovaRecanvi);
    document.getElementById('codfab_pr').addEventListener('input',f_comprovaRecanvi);
    document.getElementById('qt_pr').addEventListener('input',f_comprovaRecanvi);
    document.getElementById('preu_pr').addEventListener('input',f_comprovaRecanvi);

}

function f_comprovaRecanvi(){
    let pesa = document.getElementById('pesa_pr').value;
    let codfab = document.getElementById('codfab_pr').value;
    let qt = document.getElementById('qt_pr').value;
    let preu = document.getElementById('preu_pr').value;

    if(pesa.length==0 || codfab.length==0){
        document.getElementById('add_pr').disabled = true;
        f_validarPreu(preu,"pr_preu_error");
        f_validarQuantitats(qt,"pr_qt_error");
    }else{
        document.getElementById('add_pr').disabled = f_validarPreu(preu,"pr_preu_error") || f_validarQuantitats(qt,"pr_qt_error") || (pesa.length > 0 ? false : true) || (codfab.length > 0 ? false : true);
    }

}

function f_comprovaAltresConceptes(){
    
    /*
        En el moment d'afegir altres conceptes:
        Descripció: Obligatori
        Quantitat: Opcional(Només numeros o be formats d'aquest estil "1.5") -> Validar validarPreusQuantitats
        Preu: Opcional (Només numeros o be formats d'aquest estil "1.5") -> Validar validarPreusQuantitats
    */
    let desc = document.getElementById('desc_ac').value;
    let qt = document.getElementById('qt_ac').value;
    let preu = document.getElementById('preu_ac').value;

    if(desc.length==0){
        document.getElementById('add_ac').disabled = true;
        f_validarPreu(preu,"ac_preu_error");
        f_validarQuantitats(qt,"ac_qt_error");

    }else{    
        document.getElementById('add_ac').disabled = f_validarPreu(preu,"ac_preu_error") || f_validarQuantitats(qt,"ac_qt_error") || (desc.length > 0 ? false : true);
    }
    
}

function f_validarQuantitats(quantitat, id) {
    //Validar 0.25 0.5 0.75 o be 1 1.0 
    if(quantitat.length == 0){
        document.getElementById(id).innerHTML = "";
        return false;
    }
    const regex = /^\d+(\.(25|5|75|0))?$/;

    if (regex.test(quantitat)==false) {
        document.getElementById(id).innerHTML = "Només permeten números enters o seguit de: .0, .25 o .75";
        return true;
    } else {
        document.getElementById(id).innerHTML = "";
        return false;
    }
    
}

function f_validarPreu(preu, id) {
    if(preu.length == 0){
        document.getElementById(id).innerHTML = "";
        return false;
    }
    const regex = /^\d+(\.\d+)?$/;

    if (regex.test(preu)==false) {
        console.info('DOCUMENT: '+id);
        document.getElementById(id).innerHTML = "Només es permeten numeros amb la notació decimal amb '.'";
        return true;
    } else {
        document.getElementById(id).innerHTML = "";
        return false;
    }
}

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

                    Swal.fire({
                        icon: "success",
                        title: "Guardar reparació",
                        text: "La reparació s'ha guardat correctament, ja pots afegir les feines a realitzar",
                    });

                    //Mostrar select 
                    document.getElementById('div_dtl_select').style.display = "flex";
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

var e_definicio_tipus_linia = $('#definicio_tipus_linia');
e_definicio_tipus_linia.on('select2:select select2:unselect', function (e) {
    // Obtener los elementos seleccionados
    //var selectedOptions = select.val();
    
    document.getElementById('d_t_feines_reparacio').style.display = "flex";

    if(e_definicio_tipus_linia.val()=="-1"){
        document.getElementById('d_ac').style.display = "none";
        document.getElementById('d_p').style.display = "none";
        document.getElementById('d_pr').style.display = "none";
        document.getElementById('d_fm').style.display = "none";
    }else{
        switch(e_definicio_tipus_linia.val()){
            case "1":
                //Feines mecànic
                document.getElementById('d_fm').style.display = "flex";

                document.getElementById('d_ac').style.display = "none";
                document.getElementById('d_p').style.display = "none";
                document.getElementById('d_pr').style.display = "none";
                break;
            case "2":
                //Peces recanvi
                document.getElementById('d_pr').style.display = "flex";

                document.getElementById('d_ac').style.display = "none";
                document.getElementById('d_p').style.display = "none";
                document.getElementById('d_fm').style.display = "none";
                
                break;
            case "3":
                //Packs
                document.getElementById('d_p').style.display = "flex";

                document.getElementById('d_ac').style.display = "none";
                document.getElementById('d_pr').style.display = "none";
                document.getElementById('d_fm').style.display = "none";

                break;
            case "4":
                //Altres conceptes
                console.info('Altres conceptes');
                document.getElementById('d_ac').style.display = "flex";

                document.getElementById('d_p').style.display = "none";
                document.getElementById('d_pr').style.display = "none";
                document.getElementById('d_fm').style.display = "none";
                break;
        }
    }
    console.info(e_definicio_tipus_linia.val()); 
});

var e_packs = $('#packs');
e_packs.on('select2:select select2:unselect', function (e) {
    console.info('aa');
    f_emplenarPreuPack(e_packs.val());
    if(e_packs.val()==-1){
        document.getElementById('add_p').disabled = true;
    }else{
        document.getElementById('add_p').disabled = false;
    }
    
});


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

function f_emplenarPreuPack(id_pack){

    if(id_pack==-1){
        document.getElementById('preu_p').value = "";
    }else{
        var csrfToken = $('[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            type: 'POST',
            url: '/get_preu_pack/',
            data: {
                'id_pack': id_pack,
                'csrfmiddlewaretoken': csrfToken,
            },
            success: function(data) {
                if (data.success) {
                    //Retorn de JSON amb dades filtrades
                    console.info(data)
                    document.getElementById('preu_p').value = data.preu;
                    
                } else {
                    Swal.fire({
                        icon: "error",
                        title: "Obtenir client",
                        text: "S'ha produït un obtenint les dades del client",
                    });
                }
            },
            error: function() {
                Swal.fire({
                    icon: "error",
                    title: "Obtenir client",
                    text: "S'ha produït un obtenint les dades del client",
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