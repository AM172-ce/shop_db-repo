document.getElementById("updateInventoryForm").addEventListener("submit", function(event) {
    event.preventDefault();

    var formData = new FormData();
    formData.append("product_code", document.getElementById("product_code").value);
    formData.append("quantity_in_stock", document.getElementById("quantity_in_stock").value);

    fetch("/api/update_product_inventory", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
    
        document.getElementById("responseMessage").innerText = data.message;
    })
    .catch(error => {
        console.error("Error:", error); 

        document.getElementById("responseMessage").innerText = "An error occurred. Please try again.";
    });
});
