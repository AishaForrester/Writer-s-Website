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

   // Wait for the DOM to be fully loaded
document.addEventListener("DOMContentLoaded", function() {
    // Function to count words
    function countWords(text) {
    return text.trim().split(/\s+/).filter(word => word.length > 0).length;
    }

    // Get the textarea and the word count span...start
    const pageContent = document.getElementById("page_content");
    //const poemContent = document.getElementById("poem_content");
    
    const wordCountDisplay = document.getElementById("wordCount");
    //const wordCountPoem = document.getElementById("wordCount");

    // Initial word count update (in case there is pre-existing content)
    wordCountDisplay.textContent = countWords(pageContent.value);
    //wordCountPoem.textContent = countWords(poemContent.value);

    // Add event listener to update word count as user types: story and novel pages
    pageContent.addEventListener("input", function() {
    let wordCount = countWords(pageContent.value);
    wordCountDisplay.textContent = wordCount;
    });

    // Add event listener to update word count as user types, poems
    //poemContent.addEventListener("input", function() {
        //let wordCount = countWords(poemContent.value);
        //wordCountPoem.textContent = wordCount;
        //});
});


document.addEventListener("DOMContentLoaded", function () {
    // Retrieve the data from the div
    const projectDataDiv = document.getElementById('wordCountData');

    // Get the data from the data-* attributes
    const projectTitles = JSON.parse(projectDataDiv.getAttribute('data-project-titles'));
    const projectWordCounts = JSON.parse(projectDataDiv.getAttribute('data-word-counts'));
    const averageWordCount = JSON.parse(projectDataDiv.getAttribute('data-average-word-count'));
    const range_0_500 = JSON.parse(projectDataDiv.getAttribute('data-range-0-500'));
    const range_501_1000 = JSON.parse(projectDataDiv.getAttribute('data-range-501-1000'));
    const range_1001_1500 = JSON.parse(projectDataDiv.getAttribute('data-range-1001-1500'));
    const range_1500_plus = JSON.parse(projectDataDiv.getAttribute('data-range-1500-plus'));

    console.log(projectTitles);  // Check if the data is correct
    console.log(projectWordCounts);

    // Word Count Chart Configuration
    const wordCountData = {
        labels: projectTitles,
        datasets: [{
            label: 'Word Count',
            data: projectWordCounts,
            backgroundColor: 'rgba(54, 162, 235, 0.6)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]
    };

    const wordCountConfig = {
        type: 'bar',
        data: wordCountData,
        options: {
            responsive: true,
            indexAxis: 'y',  // Horizontal bar chart
            scales: {
                x: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Word Count'
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Project Title'
                    }
                }
            }
        }
    };

    const ctx = document.getElementById('wordCountChart').getContext('2d');
    new Chart(ctx, wordCountConfig);

    // Average Word Count Chart (Pie Chart)
    const averageWordCountChart = new Chart(document.getElementById('averageWordCountChart').getContext('2d'), {
        type: 'pie',
        data: {
            labels: ['Average Word Count'],
            datasets: [{
                data: [averageWordCount],
                backgroundColor: ['rgba(75, 192, 192, 0.6)'],
                borderColor: ['rgba(75, 192, 192, 1)'],
                borderWidth: 1
            }]
        }
    });

   
});
