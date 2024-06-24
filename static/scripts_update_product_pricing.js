document.getElementById("updatePricingForm").addEventListener("submit", function(event) {
    event.preventDefault();

    
    var formData = new FormData();
    formData.append("product_code", document.getElementById("product_code").value);
    formData.append("new_base_price", document.getElementById("new_base_price").value);
    formData.append("new_msrp", document.getElementById("new_msrp").value);

    
    fetch("/api/update_product_pricing", {
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