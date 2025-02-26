console.log("Cargando")
async function cargarDatos(){
    
    const respuesta = await fetch('data/carreras_cursos.json');
    const datos = await respuesta.json()
    console.log(datos)
}

cargarDatos()