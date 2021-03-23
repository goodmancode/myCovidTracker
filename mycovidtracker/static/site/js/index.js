const loggedOutLinks = document.querySelectorAll('.logged-out');
const loggedInLinks = document.querySelectorAll('.logged-in');

// hide/show UI elements for different login states
const setupUI = (user) => {
    if (user) {
        db.collection('users').doc(user.uid).get().then(doc => {
            details.innerHTML = `
              <div>${doc.data().email}</div>
            `;
          });

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

function setValue(uid) {
	document.getElementById("submission").value = uid;
    var state = document.getElementById("state-select").value;
    var contact = document.querySelector('input[name="contact"]:checked').value;

    // Fills result array with the selected option values
    var multi = document.getElementById("multi-select");

    var result = [];
    var options = multi && multi.options;
    var opt;

    for (var i = 0, iLen=options.length; i<iLen; i++) {
        opt = options[i];

        if (opt.selected) {
            result.push(opt.value);
        }
    }

	console.log(document.getElementById("submission").value);
    console.log(state);
    console.log(contact);
    console.log(result.includes(1));
    console.log(result.includes(2));
    console.log(result.includes(3));
    console.log(result.includes(4));
    console.log(result.includes(5));
    console.log(result.includes(6));

    return db.collection('users').doc(uid).set({
        state: state,
        loss_of_smell_and_taste: result.includes(1),
        persistent_cough: result.includes(4),
        severe_fatigue: result.includes(2),
        skipped_meals: result.includes(3),
        level_of_contact: contact,
        immuno_compromised: result.includes(5),
        vaccinated: result.includes(6)
    }, { merge: true });
}
