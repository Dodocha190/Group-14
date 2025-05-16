$(document).ready(function () {

    // --- Login Form Validation ---
    function setupLoginFormValidation() {
        const $emailInput = $('#email');
        const $passwordInput = $('#password');
        const $submitButton = $('#submit-button');

        // Function to check login form validity
        function checkLoginFormValidity() {
            const hasEmail = $emailInput.val().trim() !== '';
            const isValidEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test($emailInput.val().trim());
            const hasPassword = $passwordInput.val().trim() !== '';

            // Enable submit button only if both email and password are provided
            $submitButton.prop('disabled', !(hasEmail && hasPassword && isValidEmail));
        }

        // Disable submit button on page load
        if ($submitButton.length) {
            $submitButton.prop('disabled', true);
        }
        // Event listeners for email and password inputs to check form validity on input
        if ($emailInput.length) {
            $emailInput.on('input', checkLoginFormValidity);
        }
        if ($passwordInput.length) {
            $passwordInput.on('input', checkLoginFormValidity);
        }

    }

    // --- Sign Up Form Validation ---
    function setupSignUpFormValidation() {
        const $registerEmail = $('#email');
        const $registerPassword = $('#password');
        const $registerStudyField = $('#study-field');
        const $registerSubmit = $('#submit-button');
        const $signUpEmailError = $('.email-error-message');  // Error message elements
        const $signUpPasswordError = $('.password-error-message');

        // Function to check sign up form validity
        function checkRegisterFormValidity() {
            const hasEmail = $registerEmail.val().trim() !== '';
            const isValidEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test($registerEmail.val().trim());
            const hasPassword = $registerPassword.val().trim() !== '';
            const hasValidPassword = $registerPassword.val().length >= 6; 
            const hasStudyField = $registerStudyField.val().trim() !== '';

            // Enable submit button only if all fields are filled and passwords match
            $registerSubmit.prop('disabled', !(hasEmail && hasPassword && isValidEmail && hasValidPassword && hasStudyField));

            let isValid = true;
            let emailErrorMessage = '';
            let validPasswordErrorMessage = '';
            $signUpEmailError.text(''); 
            $signUpPasswordError.text('');

            if (hasEmail || !isValidEmail) {
                isValid = false;
                console.log('Invalid email');
                emailErrorMessage = "Please enter a valid email address.";
                $signUpEmailError.text(emailErrorMessage);
                $signUpEmailError.toggle(!hasEmail || !isValidEmail);
            }
             if (!hasValidPassword || hasPassword) {
                isValid = false;
                console.log('Invalid password');
                validPasswordErrorMessage = "Please ensure your password is 6 characters or more";
                $signUpPasswordError.text(validPasswordErrorMessage);
                $signUpPasswordError.toggle(!hasValidPassword || !hasPassword);
            }
        }


        // Disable submit button on page load
        if ($registerSubmit.length) {
            $registerSubmit.prop('disabled', true);
        }
        // Event listeners for input fields to check form validity on input
        if ($registerEmail.length) {
            $registerEmail.on('input', checkRegisterFormValidity);
        }
        if ($registerPassword.length) {
            $registerPassword.on('input', checkRegisterFormValidity);
        }
        if ($registerStudyField.length) {
            $registerStudyField.on('input', checkRegisterFormValidity);
        }
    }

    // --- Unit Search Filtering ---
    function setupUnitSearchFiltering() {
        const $unitNameInput = $('#unitNameInput');
        const $universitySelect = $('#universitySelect');
        const $searchResultsContainer = $('#searchResultsContainer');
        const $noResultsMessage = $('#noResults');
        filterUnits(); 

        // Function to filter units based on search term and selected university
        function filterUnits() {
            const searchTerm = $unitNameInput.val().toLowerCase();
            const selectedUniversity = $universitySelect.val();
            const $unitElements = $searchResultsContainer.find('.search-result-item');
            let resultsFound = 0;

            // Define a mapping of university IDs to aliases
            const universityAliases = {
                '1': ['University of Western Australia', 'UWA'],
                '2': ['Murdoch University', 'Murdoch', 'MU'],
                '3': ['Curtin University', 'Curtin', 'CU'],
                '4': ['Other']  // Keep "Other" as is
            };

            $unitElements.each(function () {
                const $this = $(this);
                const title = ($this.data('title') || '').toLowerCase(); // Get title, default to '' if undefined
                const code = ($this.data('code') || '').toLowerCase();   // Get code, default to '' if undefined
                const universityId = $this.data('university-id');

                let universityMatch = false;

                if (selectedUniversity === '') {
                    universityMatch = true; // Match all if no university is selected
                } else if (universityAliases[selectedUniversity]) {
                    // Normalize university ID for comparison
                    const normalizedUniversity = universityAliases[selectedUniversity];
                    if (Array.isArray(normalizedUniversity)) {
                        universityMatch = normalizedUniversity.includes(universityId);
                    } else {
                        universityMatch = (normalizedUniversity === selectedUniversity);
                    }
                } else if (selectedUniversity === 'Other') {
                    universityMatch = (universityId === 'Other');
                }

                // Perform the filtering logic (search term on title or code, and university)
                const titleMatch = title.includes(searchTerm);
                const codeMatch = code.includes(searchTerm);

                if ((titleMatch || codeMatch || searchTerm === '') && universityMatch) {
                    $this.show(); // Show matching units
                    resultsFound++;
                } else {
                    $this.hide(); // Hide non-matching units
                }
            });

            // Display the "No results found" message if no units match the criteria
            $noResultsMessage.css('display', resultsFound === 0 ? 'block' : 'none');
        }

        // Event listeners for the search input and university dropdown
        $unitNameInput.on('input', filterUnits);
        $universitySelect.on('change', filterUnits);
    }

    // --- Fade-in Animation for Intro and Info Boxes ---
    function setupFadeInAnimations() {
        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible'); // Add 'visible' class to trigger fade-in
                }
            });
        }, { threshold: 0.3 }); // Adjust threshold as needed

        // Observe elements with the classes 'intro-description' and 'info-box'
        document.querySelectorAll('.intro-description, .info-box').forEach(el => {
            observer.observe(el);
        });
    }

    // --- University Dropdown Style ---
    function setupUniversityDropdownStyle() {
        const universitySelect = document.getElementById('universitySelect');

        if (universitySelect) {
            universitySelect.addEventListener('change', function () {
                // Add a class when a value is selected, remove it otherwise
                universitySelect.classList.toggle('selected', this.value !== '');
            });
        }
    }

    // --- Initialize the functions ---
    setupLoginFormValidation();
    setupSignUpFormValidation();
    setupUnitSearchFiltering();
    setupFadeInAnimations();
    setupUniversityDropdownStyle();
});
