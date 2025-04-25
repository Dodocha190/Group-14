$(document).ready(function() {

/// --- For Login Form ---
    const $emailInput = $('#email');
    const $passwordInput = $('#password');
    const $submitButton = $('#submit-button');
    const $guestCheckbox = $('#guest');
    const $guestContainer = $('#continue-guest-container'); // container for the guest link
    const $guestLink = $('#continue-guest-link');
    
    function checkLoginValidation() {
        const isGuest = $guestCheckbox.prop('checked');
        const hasEmail = $emailInput.val().trim() !== '';
        const hasPassword = $passwordInput.val().trim() !== '';
        
        if (isGuest) {
            $submitButton.prop('disabled', false);
        } else if (hasEmail && hasPassword) {
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

        if ($guestContainer.length) {
            if (isGuest) {
                $guestContainer.show();
            } else {
                $guestContainer.hide();
            }
        }
    }

    $submitButton.prop('disabled', true);
    $guestCheckbox.on('change', toggleGuest);
    $emailInput.on('input', checkLoginValidation);
    $passwordInput.on('input', checkLoginValidation);
}
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

    $registerSubmit.prop('disabled', true);
    $registerEmail.on('input', checkRegisterValidation);
    $registerPassword.on('input', checkRegisterValidation);
    $registerConfirm.on('input', checkRegisterValidation);
});
