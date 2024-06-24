document.getElementById('action').addEventListener('change', function() {
    var selectedAction = this.value;
    var valueUnitFieldsDiv = document.getElementById('valueUnitFields');
    var descriptionFieldDiv = document.getElementById('descriptionField');

   
    if (selectedAction === '1') {
        valueUnitFieldsDiv.style.display = 'block';
        descriptionFieldDiv.style.display = 'none';
    } else if (selectedAction === '2') {
        valueUnitFieldsDiv.style.display = 'none';
        descriptionFieldDiv.style.display = 'block';
    } else {
        valueUnitFieldsDiv.style.display = 'none';
        descriptionFieldDiv.style.display = 'none';
    }
});

document.getElementById('productDiscountForm').addEventListener('submit', function(event) {
    event.preventDefault();  

    var formData = new FormData(this);

   
    fetch('/api/update_product_discount', {
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
      
        if (data.message) {
            document.getElementById('responseMessage').innerText = data.message;
        } else if (data.error) {
            document.getElementById('responseMessage').innerText = data.error;
        } else {
            document.getElementById('responseMessage').innerText = 'Unknown response from server.';
        }
    })
    .catch(error => {
       
        document.getElementById('responseMessage').innerText = 'An error occurred. Please try again later.';
        console.error('Error:', error);
    });
});
