document.getElementById("updateProductForm").addEventListener("submit", function(event) {
    event.preventDefault();
    var formData = new FormData(this);


    fetch("/api/fundamental_update_product", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); 
    })
    .catch(error => {
        console.error("Error:", error); 
    });
});