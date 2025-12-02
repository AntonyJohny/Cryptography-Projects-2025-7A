// SweetAlert notifications for file selection
document.addEventListener("DOMContentLoaded", function(){

    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', () => {
            if(input.files.length > 0){
                Swal.fire({
                    icon: 'info',
                    title: 'File Selected!',
                    text: `${input.files[0].name} ready for processing`,
                    timer: 2000,
                    showConfirmButton: false
                });
            }
        });
    });

    // Intercept form submissions to show loading
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            Swal.fire({
                title: 'Processing...',
                text: 'Please wait while your file is being processed.',
                allowOutsideClick: false,
                didOpen: () => Swal.showLoading()
            });
        });
    });

});
