function addToCart(button) {
    // Change the button text and background color when clicked
    button.innerHTML = 'Added Successfully';
    button.style.backgroundColor = 'green';
    

    // After 3 seconds, reset the button to its original state
    setTimeout(function() {
        button.innerHTML = 'Add to Cart';
        button.style.backgroundColor = '';
    }, 2000);  // 2000ms = 2 seconds
}


function markAsDeliver(orderId) {
    // Send an AJAX request to the backend to send OTP
    fetch(`/send_otp/${orderId}/`, {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('OTP sent successfully to customer email!');
        } else {
            alert('Failed to send OTP.');
        }
    });
}

function cancelDelivery() {
    alert('Delivery canceled.');
}







