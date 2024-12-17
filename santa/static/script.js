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

document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function () {
        document.querySelector('.nav-link.active')?.classList.remove('active');
        this.classList.add('active');
    });
});








