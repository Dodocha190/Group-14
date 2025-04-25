$(document).ready(function() {
    const $emailInput = $('#email');
    const $passwordInput = $('#password');
    const $submitButton = $('#submit-button');

    function checkLoginValidation() {
        if ($emailInput.val().trim() !== '' && $passwordInput.val().trim() !== '') {
            $submitButton.prop('disabled', false);
        } else {
            $submitButton.prop('disabled', true);
        }
    }

    $submitButton.prop('disabled', true);
    $emailInput.on('input', checkLoginValidation);
    $passwordInput.on('input', checkLoginValidation);
}
  function toggleGuest(checkbox) {
    const username = document.getElementById("username");
    const password = document.getElementById("password");
    const isGuest = checkbox.checked;

    username.disabled = isGuest;
    password.disabled = isGuest;
  });
