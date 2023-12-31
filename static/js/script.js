// Inside script.js
// ...

function displayFileName(input) {
    const outputSection = document.getElementById('outputSection');

    outputSection.innerHTML = "Uploading and analyzing..."; // Display a loading message

    // Manually trigger the form submission with the uploaded file
    uploadImage();
}

// ...

function uploadImage() {
    const fileInput = document.getElementById('fileInput');

    if (fileInput.files && fileInput.files[0]) {
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        // Use AJAX to send the file to the server
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/', true);

        // Set up the event listener to handle the response
        xhr.onload = function () {
            if (xhr.status === 200) {
                // Parse the JSON response
                try {
                    const jsonResponse = JSON.parse(xhr.responseText);

                    // Check if the expected property exists
                    if ('result_string' in jsonResponse) {
                        // Update the HTML with the response text
                        document.getElementById('outputSection').innerHTML = jsonResponse.result_string;
                    } else {
                        console.error('Missing expected property in JSON response:', jsonResponse);
                    }
                } catch (error) {
                    console.error('Error parsing JSON response:', error);
                }
            } else {
                // Handle error
                console.error('Error uploading file:', xhr.statusText);
            }
        };

        // Send the FormData containing the file to the server
        xhr.send(formData);
    }
}
