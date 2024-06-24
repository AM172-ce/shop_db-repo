document.addEventListener('DOMContentLoaded', function() {

    var today = new Date();
    var day = ("0" + today.getDate()).slice(-2);
    var month = ("0" + (today.getMonth() + 1)).slice(-2);
    var todayDate = today.getFullYear() + "-" + (month) + "-" + (day);
    var validUntilInput = document.getElementById('valid_until');
    validUntilInput.setAttribute("min", todayDate);
    validUntilInput.setAttribute("placeholder", "YYYY-MM-DD");

    document.getElementById('productDiscountForm').addEventListener('submit', function(event) {
        event.preventDefault();
        var formData = new FormData(this);

        fetch('/api/insert_product_discount', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.existing_discount) {
                document.getElementById('discountInfo').innerHTML = `
                    Product Discount Code: ${data.existing_discount.product_discount_code}<br>
                    Product Code: ${data.existing_discount.product_code}<br>
                    Discount Value: ${data.existing_discount.discount_value}<br>
                    Discount Unit: ${data.existing_discount.discount_unit}<br>
                    Valid Until: ${data.existing_discount.valid_until}<br>
                    Discount Description: ${data.existing_discount.discount_description}
                `;
                document.getElementById('existingDiscount').style.display = 'block';
                document.getElementById('responseMessage').innerText = '';  
            } else {
                document.getElementById('responseMessage').innerText = data.message;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('responseMessage').innerText = 'An error occurred. Please try again.';
        });
    });

    document.getElementById('submit').addEventListener('click', function() {
        var action = document.querySelector('input[name="action"]:checked').value;
        var product_code = document.getElementById('product_code').value;

        if (action === 'deactivate') {
            var formData = new FormData();
            formData.append('product_code', product_code);
            formData.append('action', 'deactivate');

            fetch('/api/insert_product_discount', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('responseMessage').innerText = data.message;
                document.getElementById('existingDiscount').style.display = 'none';
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('responseMessage').innerText = 'An error occurred. Please try again.';
            });
        } else if (action === 'keep') {
            document.getElementById('existingDiscount').style.display = 'none';
        } else {
            console.error('Invalid action specified.');
        }
    });
});
