document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('searchForm').addEventListener('submit', function(event) {
        event.preventDefault();

        let formData = new FormData(this);
        let params = new URLSearchParams();

        // Add form data to params, excluding empty values
        for (let [key, value] of formData.entries()) {
            if (value.trim() !== "") {
                params.append(key, value);
            }
        }

        console.log("API Request: /api/search_products?" + params.toString()); // Log the API request

        fetch(`/api/search_products?${params.toString()}`, {
            method: 'GET'
        })
        .then(response => {
            return response.json().then(data => ({ status: response.status, body: data }));
        })
        .then(({ status, body }) => {
            const resultsTableBody = document.querySelector('#resultsTable tbody');
            const responseMessageDiv = document.getElementById('responseMessage');
            resultsTableBody.innerHTML = '';
            responseMessageDiv.innerHTML = '';

            console.log("API Response:", body); // Log the API response

            if (status === 200) {
                if (body.products.length > 0) {
                    body.products.forEach(product => {
                        resultsTableBody.innerHTML += `
                            <tr>
                                <td>${product.product_code}</td>
                                <td>${product.product_name}</td>
                                <td>${product.product_vendor}</td>
                                <td>${product.base_price}</td>
                                <td>${product.quantity_in_stock}</td>
                                <td>${product.rate}</td>
                            </tr>
                        `;
                    });
                } else {
                    responseMessageDiv.innerHTML = `<p>No products found.</p>`;
                }
            } else {
                responseMessageDiv.innerHTML = `<p>Error: ${body.detail}</p>`;
            }
        })
        .catch(error => {
            const responseMessageDiv = document.getElementById('responseMessage');
            responseMessageDiv.innerHTML = `<p>Error: ${error.message}</p>`;
            console.error('Error:', error);
        });
    });
});

function goBack() {
    window.history.back();
}
