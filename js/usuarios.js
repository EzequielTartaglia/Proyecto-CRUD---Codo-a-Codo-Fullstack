const { createApp } = Vue
createApp({
data() {
return {
usuarios:[],
//url:'http://localhost:5000/usuarios',
// si el backend esta corriendo local usar localhost 5000(si no lo subieron a pythonanywhere)
url:'https://alelepere.pythonanywhere.com/usuarios', // si ya lo subieron a pythonanywhere
error:false,
cargando:true,
/*atributos para el guardar los valores del formulario */
id:0,
nombre:"",
imagen:"",
mail:"",
}
},
methods: {
fetchData(url) {
fetch(url)
.then(response => response.json())
.then(data => {
this.usuarios = data;
this.cargando=false
})
.catch(err => {
console.error(err);
this.error=true
})
},
eliminar(usuario) {
const url = this.url+'/' + usuario;
var options = {
method: 'DELETE',
}
fetch(url, options)
.then(res => res.text()) // or res.json()
.then(res => {
location.reload();
})
},
grabar(){
let usuario = {
nombre:this.nombre,
mail: this.mail,
imagen:this.imagen
}
var options = {
body:JSON.stringify(usuario),
method: 'POST',
headers: { 'Content-Type': 'application/json' },
redirect: 'follow'
}
fetch(this.url, options)
.then(function () {
alert("Registro grabado")
window.location.href = "../templates/usuarios.html";
})
.catch(err => {
console.error(err);
alert("Error al Grabarr")
})
}
},
created() {
this.fetchData(this.url)
},
}).mount('#app')