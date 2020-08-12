$('#password_help').click(function() {
    alert("This help link needs to be set up to send user email to recover password.");
});



$('#create-account').on('click', function() {
            var httpRequest;
            document.getElementById("create-account").addEventListener('click', makeRequest);

            function makeRequest() {
                httpRequest = '/create_account.html';


                httpRequest.onreadystatechange = alertContents;
                httpRequest.open('GET', '/create_accunt.html');
                httpRequest.send();
            });