const loggedOutLinks = document.querySelectorAll('.logged-out');
const loggedInLinks = document.querySelectorAll('.logged-in');

// hide/show UI elements for different login states
const setupUI = (user) => {
    if (user) {
        loggedInLinks.forEach(item => item.style.display = 'block');
        loggedOutLinks.forEach(item => item.style.display = 'none');
    } else {
        loggedInLinks.forEach(item => item.style.display = 'none');
        loggedOutLinks.forEach(item => item.style.display = 'block');
    }
};
// initialize components
document.addEventListener('DOMContentLoaded', function() {

    var modals = document.querySelectorAll('.modal');
    M.Modal.init(modals);
  
    var items = document.querySelectorAll('.collapsible');
    M.Collapsible.init(items);

    var elems = document.querySelectorAll('select');
    var instances = M.FormSelect.init(elems, {});
  
  });

function truncate(value) {
    if (value.length > 3) {
        value = value.slice(0, 3);
    }
    return value;
}

function onlyNumberKey(evt) { 
    // Only ASCII characters allowed on keypress are the digits 0-9
    var ASCIICode = (evt.which) ? evt.which : evt.keyCode 
    if (ASCIICode > 31 && (ASCIICode < 48 || ASCIICode > 57)) {
        //$('#modal-invalid').modal('open');
        // alert("Enter a number");
        M.toast({html: 'Please enter a number', displayLength: 1000})
        return false; 	  
    }
    return true; 
} 

// module.exports = truncate, onlyNumberKey
