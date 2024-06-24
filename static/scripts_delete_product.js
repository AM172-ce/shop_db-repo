document.getElementById('deleteProductForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var formData = new FormData(this);
    fetch('/api/delete_product', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        
        document.getElementById('responseMessage').innerText = data.message;
    })
    .catch(error => {
        
        document.getElementById('responseMessage').innerText = 'An error occurred. Please try again later.';
        console.error('Error:', error);
    });
});