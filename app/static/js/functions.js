// For login and signup pages ===
$(document).ready(function() {
    const $emailInput = $('#email');
    const $passwordInput = $('#password');
    const $submitButton = $('#submit-button');
     const $guestCheckbox = $('#guest'); //check if checkbox has the id 'guest'
    
    function checkLoginValidation() {
        const isGuest = $guestCheckbox.prop('checked');
        const hasUsername = $usernameInput.val().trim() !== '';
        const hasPassword = $passwordInput.val().trim() !== '';
        
        if (isGuest) {
            $submitButton.prop('disabled', false);
        } else if (hasUsername && hasPassword) {
            $submitButton.prop('disabled', false);
        } else {
            $submitButton.prop('disabled', true);
        }
    }

    function toggleGuest() {
        const isGuest = $guestCheckbox.prop('checked');

        $usernameInput.prop('disabled', isGuest);
        $passwordInput.prop('disabled', isGuest);
        checkLoginValidation();  // re-check validation status
    }

    $submitButton.prop('disabled', true);
    $guestCheckbox.on('change', toggleGuest);
    $emailInput.on('input', checkLoginValidation);
    $passwordInput.on('input', checkLoginValidation);
});

// For both home pages ===

document.addEventListener('DOMContentLoaded', () => {
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.3 });

    document.querySelectorAll('.intro-description, .card').forEach(el => {
        observer.observe(el);
    });

    const universitySelect = document.getElementById('university-select');

    if (universitySelect) {
        universitySelect.addEventListener('change', function() {
            if (universitySelect.value) {
                universitySelect.classList.add('selected');
            } else {
                universitySelect.classList.remove('selected');
            }
        });
    }
});
