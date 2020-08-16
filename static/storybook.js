$("#password_help").on('click', () => {
    alert("This help link needs to be set up to send user email to recover password.");
});


$(document).ready(function() {
    if ($.fn.cloudinary_fileupload !== undefined) {
        $("input.cloudinary-fileupload[type=file]").cloudinary_fileupload();
    }
});

var cl = new cloudinary.Cloudinary({ cloud_name: "juliepitman", secure: true });


dialog.addEventListener('imageuploader.fileready', function(ev) {
    // Upload a file to Cloudinary
    var formData;
    var file = ev.detail().file;

    // Define functions to handle upload progress and completion
    function xhrProgress(ev) {
        // Set the progress for the upload
        dialog.progress((ev.loaded / ev.total) * 100);
    }

    function xhrComplete(ev) {
        var response;

        // Check the request is complete
        if (ev.target.readyState != 4) {
            return;
        }

        // Clear the request
        xhr = null
        xhrProgress = null
        xhrComplete = null

        // Handle the result of the upload
        if (parseInt(ev.target.status) == 200) {
            // Unpack the response (from JSON)
            response = JSON.parse(ev.target.responseText);

            // Store the image details
            image = {
                angle: 0,
                height: parseInt(response.height),
                maxWidth: parseInt(response.width),
                width: parseInt(response.width)
            };

            // Apply a draft size to the image for editing
            image.filename = parseCloudinaryURL(response.url)[0];
            image.url = buildCloudinaryURL(
                image.filename, [{ c: 'fit', h: 600, w: 600 }]
            );

            // Populate the dialog
            dialog.populate(image.url, [image.width, image.height]);

        } else {
            // The request failed, notify the user
            new ContentTools.FlashUI('no');
        }
    }

    // Set the dialog state to uploading and reset the progress bar to 0
    dialog.state('uploading');
    dialog.progress(0);

    // Build the form data to post to the server
    formData = new FormData();
    formData.append('file', file);
    formData.append('upload_preset', CLOUDINARY_PRESET_NAME);

    // Make the request
    xhr = new XMLHttpRequest();
    xhr.upload.addEventListener('progress', xhrProgress);
    xhr.addEventListener('readystatechange', xhrComplete);
    xhr.open('POST', CLOUDINARY_UPLOAD_URL, true);
    xhr.send(formData);
});