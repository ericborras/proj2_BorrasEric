// Datos de ejemplo para la tabla

    // Número de registros por página
    const TOTAL_REGISTRES_PAGINA = 20;
    const BTN_PAGINACIO = 4; // Número máximo de botones de página a mostrar
    var data
    $(document).ready(function() {
        // Handler for .ready() called.
        var reparacions_str = config.reparacions;
        var reparacions_str_f = reparacions_str.replace(/'/g, '"');
        data = JSON.parse(reparacions_str_f);
        generatePagination(1, data);
        displayData(1, data);
    
        $(document).ready(function() {
            $('.js-example-basic-multiple').select2();
        });
    
        
        document.getElementById('b_elimina_filtres').addEventListener('click',f_eliminaFiltres);
    
        document.getElementById('f_data_alta').addEventListener('change',f_filtraReparacions);
    
        try{
            var select = $('#f_estat');
            // Agregar un event listener para el evento change de Select2
            select.on('select2:select select2:unselect', function (e) {
                // Obtener los elementos seleccionados
                //var selectedOptions = select.val();
                f_filtraReparacions();
            });
        }catch(e){};
        
        document.getElementById('f_marca_model').addEventListener('input',f_filtraReparacions);
        document.getElementById('f_matricula').addEventListener('input',f_filtraReparacions);
        document.getElementById('f_client').addEventListener('input',f_filtraReparacions);
        document.getElementById('f_poblacio').addEventListener('input',f_filtraReparacions);
        document.getElementById('f_nif').addEventListener('input',f_filtraReparacions);
        try{
            document.getElementById('f_pagada').addEventListener('change',f_filtraReparacions);
        }catch(e){};
        
    });
    
    function f_filtraReparacions(){
        let f_data_alta = document.getElementById('f_data_alta').value;
        let f_estat = "";
        try{
            //f_estat = $('#f_estat').val();
            f_estat = $('#f_estat').val() ? $('#f_estat').val().join(',') : '';
        }catch(e){};
        
        let f_marca_model = document.getElementById('f_marca_model').value;
        let f_matricula = document.getElementById('f_matricula').value;
        let f_client = document.getElementById('f_client').value;
        let f_poblacio = document.getElementById('f_poblacio').value;
        let f_nif = document.getElementById('f_nif').value;
        let f_pagada = false; 
        try{
            f_pagada = document.getElementById('f_pagada').checked;
        }catch(e){};
    
        console.info("F_ESTAT: "+f_estat);
        
        var csrfToken = $('[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            type: 'POST',
            url: '/filtrar_reparacions/',
            data: {
                'f_data_alta': f_data_alta,
                'f_estat': f_estat,
                'f_marca_model': f_marca_model,
                'f_matricula': f_matricula,
                'f_client': f_client,
                'f_poblacio': f_poblacio,
                'f_pagada': f_pagada,
                'f_nif': f_nif,
                'csrfmiddlewaretoken': csrfToken,
            },
            success: function(data) {
                if (data.success) {
                    //Retorn de JSON amb dades filtrades
                    console.info(data.data)
                    generatePagination(1, data.data);
                    displayData(1, data.data);
                } else {
                    Swal.fire({
                        icon: "error",
                        title: "Filtrar reparacions",
                        text: "S'ha produït un error filtrant les reparacions",
                    });
                }
            },
            error: function() {
                Swal.fire({
                    icon: "error",
                    title: "Filtrar reparacions",
                    text: "S'ha produït un error filtrant les reparacions",
                });
            }
        });
    
    }
    
    function f_eliminaFiltres(){
        document.getElementById('f_data_alta').value = "";
        document.getElementById('f_marca_model').value = "";
        document.getElementById('f_matricula').value = "";
        document.getElementById('f_client').value = "";
        document.getElementById('f_poblacio').value = "";
        document.getElementById('f_pagada').checked = false;
        document.getElementById('f_nif').value = "";
    
        var select2Element = $('#f_estat');
        // Desseleccionar todas las opciones
        select2Element.val(null).trigger('change');
    
        //Establir taula estat inicial
        generatePagination(1, data);
        displayData(1, data);
        
    }
    
    // Función para mostrar los datos paginados
    function displayData(pageNum, data) {
        var table = document.getElementById('myTable').getElementsByTagName('tbody')[0];
        table.innerHTML = '';
        var start = (pageNum - 1) * TOTAL_REGISTRES_PAGINA;
        var end = Math.min(start + TOTAL_REGISTRES_PAGINA, data.length);
        for (var i = start; i < end; i++) {
            var row = table.insertRow();
            row.insertCell(0).innerHTML = data[i].data_alta;
            row.insertCell(1).innerHTML = data[i].estat_reparacio;
            row.insertCell(2).innerHTML = '('+data[i].matricula+') '+ data[i].marca_model;
            row.insertCell(3).innerHTML = data[i].nom + ' ' + data[i].cognoms + ' (' + data[i].nif + ')' + ' - ' + data[i].telefon+' ('+data[i].ciutat+")";
            row.insertCell(4).innerHTML = data[i].nom_usuari + ' (' + data[i].tipus_usuari + ')';
    
            console.info("URL_REPARACIÓ "+data[i].url_reparacio+" AAA: "+data[i].id)
            //url_reparacio
            let a = document.createElement('a');
            a.href = data[i].url_reparacio;
    
            // Crear el elemento <button> dinámicamente
            var btn = document.createElement('button');
    
            // Establecer las clases y el título del botón
            btn.className = 'b_elimina_filtre';
            btn.title = 'Obrir reparació';
    
            // Crear el elemento <i> para el ícono del botón
            var icon = document.createElement('i');
            icon.className = 'fa-solid fa-wrench';
    
            // Agregar el icono al botón
            btn.appendChild(icon);
    
            // Agregar el botón al enlace
            a.appendChild(btn);
    
            row.insertCell(5).appendChild(a);
            row.insertCell(6).innerHTML = ''; // Ajusta esto según tus necesidades
    
            /*
            <a href="">
                <button class="b_elimina_filtre" title="Obrir reparació">
                    <i class="fa-solid fa-plus fa-xl"></i>
                </button>
            </a>
            */
        }
    }
    
    // Función para generar el paginador
    function generatePagination(currentPage, data) {
        var pagination = document.getElementById('pagination');
        pagination.innerHTML = '';
        var pageCount = Math.ceil(data.length / TOTAL_REGISTRES_PAGINA);
    
        var startPage = Math.max(currentPage - Math.floor(BTN_PAGINACIO / 2), 1);
        var endPage = Math.min(startPage + BTN_PAGINACIO - 1, pageCount);
        if (endPage - startPage < BTN_PAGINACIO - 1) {
            startPage = Math.max(endPage - BTN_PAGINACIO + 1, 1);
        }
        if (startPage > 1) {
            addNavigationButton('Prev', currentPage - 1, data);
            addNavigationButton('<<', 1, data); // Botón para ir al principio
        }
        for (var i = startPage; i <= endPage; i++) {
            addButton(i, currentPage, data);
        }
        if (endPage < pageCount) {
            addNavigationButton('>>', pageCount, data); // Botón para ir al final
            addNavigationButton('Següent', currentPage + 1, data);
        }
    }
    
    // Función auxiliar para agregar botones de página al paginador
    function addButton(pageNum, currentPage, data) {
        var button = document.createElement('button');
        button.textContent = pageNum;
        if (pageNum === currentPage) {
            button.classList.add('active');
        }
        button.addEventListener('click', function(event) {
            var pageNum = parseInt(event.target.textContent);
            displayData(pageNum, data);
            generatePagination(pageNum, data);
        });
        pagination.appendChild(button);
    }
    
    // Función auxiliar para agregar botones de navegación al paginador
    function addNavigationButton(label, pageNum, data) {
        var button = document.createElement('button');
        button.textContent = label;
        button.addEventListener('click', function() {
            displayData(pageNum, data);
            generatePagination(pageNum, data);
        });
        pagination.appendChild(button);
    }