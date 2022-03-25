$(document).on('submit','#remember',function(){
   // code

   	alert();
   	$.ajax({
		type:"POST", // la variable type guarda el tipo de la peticion GET,POST,..
    	url:"http://localhost:5000/keywordextract/", //url guarda la ruta hacia donde se hace la peticion
    	data:{url:"https://www.subrayado.com.uy/rodeado-sus-hijos-moreira-nego-acoso-sexual-y-dijo-que-no-renuncia-la-intendencia-n562316"}, // data recive un objeto con la informacion que se enviara al servidor
    	success:function(datos){ //success es una funcion que se utiliza si el servidor retorna informacion
        	console.log(datos);
     	},
     	
	})
});