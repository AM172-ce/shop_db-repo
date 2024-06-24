document.getElementById('deleteProductDiscountForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var formData = new FormData(this);
    fetch('/api/delete_product_discount', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
    
    })
    .catch(error => {
        console.error('Error:', error);
    });
});