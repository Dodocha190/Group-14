$(document).ready(function () {

    // --- For Login Form ---
    const $emailInput = $('#email');
    const $passwordInput = $('#password');
    const $submitButton = $('#submit-button');
    const $guestCheckbox = $('#guest');
    const $guestContainer = $('#continue-guest-container'); // container for the guest link
    const $guestLink = $('#continue-guest-link');

    function checkLoginValidation() {
        const isGuest = $guestCheckbox.length && $guestCheckbox.prop('checked');
        const hasEmail = $emailInput.val().trim() !== '';
        const hasPassword = $passwordInput.val().trim() !== '';

        if (isGuest || (hasEmail && hasPassword)) {
            $submitButton.prop('disabled', false);
        } else {
            $submitButton.prop('disabled', true);
        }
    }

    function toggleGuest() {
        const isGuest = $guestCheckbox.prop('checked');

        $emailInput.prop('disabled', isGuest);
        $passwordInput.prop('disabled', isGuest);
        checkLoginValidation();
    }

    if ($submitButton.length) {$submitButton.prop('disabled', true);}
    if ($guestCheckbox.length) {$guestCheckbox.on('change', toggleGuest);}
    if ($emailInput.length) {$emailInput.on('input', checkLoginValidation);}
    if ($passwordInput.length) {$passwordInput.on('input', checkLoginValidation);}
    
    if ($guestLink.length && $guestCheckbox.length) {
        $guestLink.on('click', function (e) {
            e.preventDefault();
            if (!$guestCheckbox.prop('checked')) {
                $guestCheckbox.prop('checked', true).trigger('change');
            }
        });
    }

    // --- For Sign Up Form ---
    const $registerEmail = $('#register-email');
    const $registerPassword = $('#register-password');
    const $registerConfirm = $('#register-confirm');
    const $registerSubmit = $('#register-submit');

    function checkRegisterValidation() {
        const hasEmail = $registerEmail.val().trim() !== '';
        const hasPassword = $registerPassword.val().trim() !== '';
        const hasConfirm = $registerConfirm.val().trim() !== '';
        const passwordsMatch = $registerPassword.val() === $registerConfirm.val();

        if (hasEmail && hasPassword && hasConfirm && passwordsMatch) {
            $registerSubmit.prop('disabled', false);
        } else {
            $registerSubmit.prop('disabled', true);
        }
    }

    if ($registerSubmit.length) {$registerSubmit.prop('disabled', true);}
    if ($registerEmail.length) {$registerEmail.on('input', checkRegisterValidation);}
    if ($registerPassword.length) {$registerPassword.on('input', checkRegisterValidation);}
    if ($registerConfirm.length) {$registerConfirm.on('input', checkRegisterValidation);}
});

document.addEventListener('DOMContentLoaded', () => {
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.3 });

    document.querySelectorAll('.intro-description, .info-box').forEach(el => {
        observer.observe(el);
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const universitySelect = document.getElementById('university-select');

    universitySelect.addEventListener('change', function() {
        if (universitySelect.value) {
            universitySelect.classList.add('selected');
        } else {
            universitySelect.classList.remove('selected');
        }
    });
});
