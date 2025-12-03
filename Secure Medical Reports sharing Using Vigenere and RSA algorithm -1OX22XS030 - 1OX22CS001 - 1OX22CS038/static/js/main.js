// Small global JS helpers
document.addEventListener('DOMContentLoaded', function () {
  // Simple flash message display using SweetAlert if element with id=flash exists
  const flash = document.getElementById('flash');
  if (flash && flash.dataset && flash.dataset.message) {
    Swal.fire({ icon: flash.dataset.type || 'info', title: flash.dataset.message, timer: 2000, showConfirmButton: false });
  }
});