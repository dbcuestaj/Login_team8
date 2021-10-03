var nombre=prompt("cual es tu nombre: ");
var apellido=prompt("Apellido: ");
var old=parseInt(prompt("Cual es tu edad: "));

if (old>=18){
    document.write(nombre + " " + apellido + " es matoy de edad");
}else{
    document.write(nombre + " " + apellido +" "+ "Eres un baby, tienes"+" "+old);
}