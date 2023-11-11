var isDarkMode = false; // Variable para realizar un seguimiento del modo actual

// Función para cambiar entre los modos claro y oscuro
function toggleMode() {
    isDarkMode = !isDarkMode; // Cambia el valor del modo
    var bodyElement = document.body;
    var modeIcon = document.getElementById("mode-icon");
    var logo = document.getElementById("logo");

    if (isDarkMode) {
        bodyElement.classList.add("dark-mode");
        bodyElement.classList.remove("light-mode");
        modeIcon.src = "/static/oscuro-claro.png";
        logo.src = "/static/logo-oscuro.png";
    } else {
        bodyElement.classList.add("light-mode");
        bodyElement.classList.remove("dark-mode");
        modeIcon.src = "/static/claro-oscuro.png";
        logo.src = "/static/logo-claro.png";
    }
}

function updateConversation(message) {
    var conversationDiv = document.getElementById("conversation");
    var userMessageHTML = "<p><strong>Tú:</strong> " + message.user_input + "</p>";
    conversationDiv.innerHTML += userMessageHTML;

    if (message.bot_response) {
        var botMessageHTML = "<p><strong>Bot:</strong> " + message.bot_response + "</p>";
        conversationDiv.innerHTML += botMessageHTML;
    }
}

// Evento para cambiar el modo cuando se hace clic en el botón
document.getElementById("toggle-mode-button").addEventListener("click", toggleMode);

// Función para mostrar una alerta cuando se intenta recargar la página
window.addEventListener("beforeunload", function (e) {
    var confirmationMessage = "¿Seguro que deseas recargar la página? Los datos no guardados se perderán.";
    if (typeof e === 'undefined') {
        e = window.event;
    }
    if (e) {
        e.returnValue = confirmationMessage;
    }
    return confirmationMessage;
});

// Evento para manejar el envío del formulario de entrada del usuario y la actualización de la conversación en la página
document.querySelector("form").onsubmit = function (event) {
    event.preventDefault();
    var user_input = document.querySelector("input[name=user_input]").value;
    fetch("/send_message", {
        method: "POST",
        body: new URLSearchParams({ user_input: user_input }),
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
    }).then(function (response) {
        return response.text();
    }).then(function (responseText) {
        updateConversation({ user_input: user_input, bot_response: responseText });
    });
    document.querySelector("input[name=user_input]").value = "";
}
