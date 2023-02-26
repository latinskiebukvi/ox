function sendFormData() {
    const formElement = document.querySelector("form");
    user_id = new FormData(formElement).get("user_id")

    fetch('/', {
        method: 'POST',
        body: JSON.stringify({
            "id": user_id
        })
    })
    .then(function(response) {
        window.location.replace(response.url)
    })
}