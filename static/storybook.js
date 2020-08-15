$("#password_help").on('click', () => {
    alert("This help link needs to be set up to send user email to recover password.");
});


$(document).ready(function() {
    if ($.fn.cloudinary_fileupload !== undefined) {
        $("input.cloudinary-fileupload[type=file]").cloudinary_fileupload();
    }
});

var cl = new cloudinary.Cloudinary({ cloud_name: "juliepitman", secure: true });