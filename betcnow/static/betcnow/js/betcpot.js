function llenar_matriz(centena) {    
    var lista = lista_status;   //Recibe la lista con los estados de las jugadas en la BD. 1=Free; 2 y 3 = Ocupados
    var html = '';  //String con código html que retornará la función
    var table = document.getElementById('tabla_jugadas');   //La tabla donde se van reportando las jugadas seleccionadas
    var parada = parseInt(centena)+100      //Criterio de parada (se recibe el parámetro centena que es un string)
    var color;      //Verde si está free, rojo si está ocupado
    var disabled = false;   //Boolean para evitar que se presione un número que ya ha sido escogido
    for (i=centena; i<parada; i++){
        if (lista[i] == 1){         //Verde
            color = "'btn btn-success custom'";     
        }
        else{           //Rojo
            color = "'btn btn-danger custom'";
            disabled = true;
        }

        for (var j = 1, row; row = table.rows[j]; j++){    //Si la jugada ya está en la tabla de seleccionadas, se desactiva el numero 
            if (i == row.cells[0].children[0].value){
                disabled = true;

            }
        }
                //Cada iteración construye un botón
        html += "<input type='button' class=" + color + " value='" + i + "' onclick='this.disabled=true; add_jugada(" + i + ")'";                
        if (disabled == true){      
            html += " disabled=true";
        }

        html += "/>";
        disabled = false;
    }
    $('#matriz').html(html);                                

    }

function add_jugada(i) {            //Añadir jugada a la tabla de seleccionadas
    var table = document.getElementById('tabla_jugadas');
    document.getElementById('cant_jugadas').innerHTML = table.rows.length;  //El texto que dice cuantas jugadas has seleccionado
    var row = table.insertRow(-1);  //Insertar al final
    var cell1 = row.insertCell(0);       //Celda 1, la jugada    
    cell1.innerHTML = "<input type='text' name='jugadas[]' class='form-control' readonly=true value='" + i + "'/>";
    var cell2 = row.insertCell(1);      //Celda 2, el botón de delete
    cell2.innerHTML = "<button type='button' class='btn btn-default' onclick='delete_row(this)'>Delete</button>";
}

function delete_row(elemento) {      //Recibe de parámetro un elemento de tipo Object
    cell = elemento.parentNode; //Se sube un nivel a la celda donde está el object
    row = cell. parentNode;     //Se sube un nivel a la fila donde está la celda
    valor = row.cells[0].children[0].value;     //Se recupera el número de la jugada
    row.remove();       //Se elimina la fila
    llenar_matriz(Math.trunc(valor/100)*100);   //Se actualiza la matriz
    var tr = $('#tabla_jugadas tr').length - 1; //Se actualiza texto cuantas jugadas llevas (-1 porque el propio texto ya es una fila)
    $('#cant_jugadas').text(tr);
}

function random_values() {
    var random_times = $("#random_input").val(); //Se lee el valor ingresado en la input
    var x;  
    if (random_times > 0 && random_times<=8){     //Se valida lo ingresado
        for (var i=0; i < random_times; i++){      
            var x = Math.floor((Math.random() * 1000) + 0);
            add_jugada(x);                        //Se añade una jugada a la tabla, random_times cantidad de veces
        }
        centena = Math.trunc(x/100)*100;        //Se calcula la centena del numero random
        llenar_matriz(centena);     //Se actualiza la matríz
    }
    else {
        alert("Invalid amount of random numbers")
    }
}        
