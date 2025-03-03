document.addEventListener("DOMContentLoaded", function() {
    const slides = document.querySelectorAll('.text');
    let current_index = 0;
    let total_slides = slides.length;

    //quotes
    const quotes = document.querySelectorAll(".quotes_next1");
    let currentIndex = 0;

    // Function to show the next quote
    function showNextQuote() {
        // Hide the current quote
        quotes[currentIndex].classList.remove("active");
        quotes[currentIndex].style.opacity = "0";

        // Update index to the next quote
        currentIndex = (currentIndex + 1) % quotes.length;

        // Show the next quote
        quotes[currentIndex].classList.add("active");
        quotes[currentIndex].style.opacity = "1";
    }

    // Set the initial state
    quotes.forEach((quote, index) => {
        //if the quote is 0 we set the opacity to 1, othere will be 0
        quote.style.opacity = index === 0 ? "1" : "0";
        if (index === 0) quote.classList.add("active");
    });

    // Change quote every 3 seconds
    setInterval(showNextQuote, 3000);
    //************************************** */

    

    function showSlide() {
        // Hide all slides and reset position
        slides.forEach(slide => {
            slide.style.opacity = '0';
            slide.style.transform = 'translateX(100%)'; // Start off-screen to the right
        });

        // Show the current slide
        slides[current_index].style.opacity = '1';
        slides[current_index].style.transform = 'translateX(0)'; // Bring it into view

        // Move to the next slide
        current_index++;
        if (current_index >= total_slides) {
            current_index = 0; // Loop back to the first slide
        }
    }

    // Start the animation
    function startAnimation() {
        showSlide();

        // Slide the current slide out to the left after 3 seconds
        setTimeout(() => {
            slides[current_index].style.transform = 'translateX(-100%)'; // Slide out to the left
        }, 1000); // Wait for 3 seconds before sliding out

        // Loop through the slides continuously every 3 seconds
        setTimeout(startAnimation, 2000);
    }

    // Start the animation immediately
    startAnimation();

    //javaScript to toggle the dropdown visibility 
    document.getElementById("createText").addEventListener("click", function() {
        var dropdown = document.getElementById("createDropdown");
        // Toggle the dropdown's display
        dropdown.style.display = (dropdown.style.display === "none" || dropdown.style.display === "") ? "block" : "none";
    });


  
});

document.addEventListener("DOMContentLoaded", function() {

    // When the "Create" button is clicked, show the modal
    const createButton = document.querySelector('#createText');
    if (createButton) {
        createButton.addEventListener('click', function() {
            showModal();
        });
    }

    // Show the modal and apply the blur effect
    function showModal() {
        const popupModal = document.getElementById("popupModal");
        if (popupModal) {
            popupModal.style.display = "flex";
            document.body.classList.add('modal-open');
        }
    }

    // Close the modal when the close button is clicked
    const closePopupButton = document.getElementById("closePopup");
    if (closePopupButton) {
        closePopupButton.addEventListener("click", function() {
            closeModal();
        });
    }

    // Close the modal if the user clicks outside of the modal content
    const popupModal = document.getElementById("popupModal");
    if (popupModal) {
        popupModal.addEventListener("click", function(event) {
            // Check if the user clicked outside the modal content
            if (event.target === popupModal) {
                closeModal();
            }
        });
    }

    // Function to close the modal
    function closeModal() {
        const popupModal = document.getElementById("popupModal");
        if (popupModal) {
            popupModal.style.display = "none";
            document.body.classList.remove('modal-open');
        }
    }


    // Prevent modal from closing on form submit (if needed)
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(event) {
            // Ensure form submission happens correctly
            event.preventDefault();
            form.submit();
        });
    }

});


document.addEventListener("DOMContentLoaded", function() {
    // Function to format time as hh:mm AM/PM
    function formatTime(date) {
        let hours = date.getHours();
        let minutes = date.getMinutes().toString().padStart(2, '0');
        let period = hours >= 12 ? 'PM' : 'AM'; // Determine AM or PM

        // Convert hours to 12-hour format
        hours = hours % 12;
        hours = hours ? hours : 12; // Handle the case of 0 being converted to 12

        return `${hours}:${minutes} ${period}`;
    }

    // Update the time immediately when the page loads
    const timeElement = document.getElementById('current-time');
    const currentTime = new Date();
    timeElement.textContent = formatTime(currentTime);

    // Update the time every minute
    setInterval(() => {
        const currentTime = new Date();
        timeElement.textContent = formatTime(currentTime);
    }, 60000); // Update every 60 seconds
});