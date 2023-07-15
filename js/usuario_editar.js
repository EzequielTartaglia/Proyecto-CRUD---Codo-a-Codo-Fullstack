console.log(location.search) // lee los argumentos pasados a este formulario
var id=location.search.substr(4)
console.log(id)
const { createApp } = Vue
createApp({
data() {
return {
id:0,
nombre:"",
imagen:"",
mail:"",
url:'https://alelepere.pythonanywhere.com/usuarios/'+id,
}
},
methods: {
fetchData(url) {
fetch(url)
.then(response => response.json())
.then(data => {

console.log(data)
this.id=data.id
this.nombre = data.nombre;
this.imagen=data.imagen
this.mail=data.mail
})
.catch(err => {
console.error(err);
this.error=true
})
},
modificar() {
let usuario = {
nombre:this.nombre,
mail: this.mail,
imagen:this.imagen
}
var options = {
body: JSON.stringify(usuario),
method: 'PUT',
headers: { 'Content-Type': 'application/json' },
redirect: 'follow'
}
fetch(this.url, options)
.then(function () {
alert("Registro modificado")
window.location.href = "../templates/usuarios.html";
})
.catch(err => {
console.error(err);
alert("Error al Modificar")
})
}
},
created() {
this.fetchData(this.url)
},
}).mount('#app')