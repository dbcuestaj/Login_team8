let nombre = document.getElementById("name")
let password = document.getElementById("Pw")

function login_1() {
    if (password.value.length() < 8) {
        alert("la contraseña debe tener más de 8 digitos")
    }

}