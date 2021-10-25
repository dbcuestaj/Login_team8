function Registro() {
    input_contrasena = document.getElementById('contraseña')
    input_confirmar_contrasena = document.getElementById('contraseña2')

    if (!validar_contrasena(input_contrasena.value)) {
        alert('La contrasena debe tener minimo 8 caracteres, una letra mayuscula, una letra minuscula y un caracter especial')
        return false
    }
    if (!(input_contrasena.value == input_confirmar_contrasena.value)) {
        alert('Las contrasenas no coinciden')
        return false
    }
}

function validar_contrasena(contrasena) {
    if (/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/i.test(contrasena)) {
        return true
    } else {
        return false
    }
}