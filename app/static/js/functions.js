$(document).ready(function() {
    const $usernameInput = $('#username');
    const $passwordInput = $('#password');
    const $submitButton = $('#submit-button');

    function checkLoginValidation() {
        if ($usernameInput.val().trim() !== '' && $passwordInput.val().trim() !== '') {
            $submitButton.prop('disabled', false);
        } else {
            $submitButton.prop('disabled', true);
        }
    }

    $submitButton.prop('disabled', true);

    $usernameInput.on('input', checkLoginValidation);
    $passwordInput.on('input', checkLoginValidation);
});