document.addEventListener('DOMContentLoaded', function() {
    // Get elements
    const submitPwChangeBtn = document.getElementById('submitPwChange');
    const cancelPwChangeBtn = document.getElementById('cancelPwChange');
    
    // Handle form submission
    submitPwChangeBtn.addEventListener('click', function() {
        // Collect form data
        const username = document.getElementById('username').value.trim();
        const oldPassword = document.getElementById('old_password').value.trim();
        const newPassword = document.getElementById('new_password').value.trim();
        const newPassword2 = document.getElementById('new_password2').value.trim();

        // Validate form data
        if (!username || !oldPassword || !newPassword || !newPassword2) {
            alert('Please fill in all fields.');
            return;
        }

        if (newPassword !== newPassword2) {
            alert('New passwords do not match.');
            return;
        }

        // Prepare data for API request
        const requestData = {
            username: username,
            password: oldPassword,
            new_password: newPassword,
            api_key: 'your_api_key_here', // Replace with actual API key or retrieve from session
            action: 'changepassword'
        };

        // Send request to API
        fetch('/api/user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
            } else {
                alert('Password changed successfully!');
                // Optionally, clear form fields
                document.getElementById('username').value = '';
                document.getElementById('old_password').value = '';
                document.getElementById('new_password').value = '';
                document.getElementById('new_password2').value = '';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while changing the password.');
        });
    });

    // Handle cancel button
    cancelPwChangeBtn.addEventListener('click', function() {
        // Optionally, clear form fields or redirect
        document.getElementById('username').value = '';
        document.getElementById('old_password').value = '';
        document.getElementById('new_password').value = '';
        document.getElementById('new_password2').value = '';
    });
});
