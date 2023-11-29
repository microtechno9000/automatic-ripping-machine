// Event listener for the Session edit scripts
 document.addEventListener('DOMContentLoaded', function () {
     var form = document.getElementById('sessionstatus');
     form.addEventListener('change', function () {
         saveForm(event.target);
     });
 });

// Save the form data (active and drive info) to the database
function saveForm(field) {
    var formData = {};
    formData.id = field.id;

    // Check if a checkbox and set true or false
    if (field.type === 'checkbox') {
        var checkbox = document.getElementById(field.id);
        formData.value = checkbox.checked;
    } else {
        formData.value = field.value;
    }

    // Add the CSRF token to the formData
    var csrfToken = document.getElementById('csrf_token').getAttribute('value');

    console.log('Field with ID ' + field.id + ' has changed. New value: ' + formData[field.id]);

    fetch('/session/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken, // Include this line
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success === true) {
            document.getElementById('successAlert').innerHTML = `<strong>Success:</strong> ${data.response}`;
            document.getElementById('successAlert').style.display = 'block';
            document.getElementById('errorAlert').style.display = 'none';
        } else {
            if (data.clear === true) {
                document.getElementById(field.id).selectedIndex = 0;
            }
            document.getElementById('errorAlert').innerHTML = `<strong>Error:</strong> ${data.response}`;
            document.getElementById('errorAlert').style.display = 'block';
            document.getElementById('successAlert').style.display = 'none';
        }

        // Handle the server response as needed
        console.log('Server response:', data);
    })
    .catch(error => {
        console.error('Error:', error);

        document.getElementById('successAlert').style.display = 'none';
        document.getElementById('errorAlert').style.display = 'block';
    });
}