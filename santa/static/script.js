
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



  function getAddressSuggestions() {
    const input = document.getElementById('suggested_address');
    const query = input.value;

    if (query.length < 3) {
        document.getElementById('suggestions-list').innerHTML = '';
        return;
    }

    const geocodeUrl = `https://maps.googleapis.com/maps/api/geocode/json?address=${query}&key=YOUR_GOOGLE_API_KEY`;

    fetch(geocodeUrl)
        .then(response => response.json())
        .then(data => {
            const suggestionsList = document.getElementById('suggestions-list');
            suggestionsList.innerHTML = '';

            if (data.status === 'OK') {
                data.results.forEach(result => {
                    const suggestionItem = document.createElement('li');
                    suggestionItem.textContent = result.formatted_address;
                    suggestionItem.onclick = () => {
                        input.value = result.formatted_address;
                        document.getElementById('suggestions-list').innerHTML = '';
                    };
                    suggestionsList.appendChild(suggestionItem);
                });
            }
        });
  }











