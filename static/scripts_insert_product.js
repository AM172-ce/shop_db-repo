document.addEventListener('DOMContentLoaded', () => {
    const productForm = document.getElementById('productForm');
    const responseMessage = document.getElementById('responseMessage');

    if (productForm) {
        productForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const formData = new FormData(productForm);
            const url = '/api/insert_product'; 
            
            try {
                const response = await fetch(url, {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const data = await response.json();
                responseMessage.textContent = data.message;
            } catch (error) {
                responseMessage.textContent = error.message;
            }
        });
    } else {
        console.error('productForm not found');
    }
});
