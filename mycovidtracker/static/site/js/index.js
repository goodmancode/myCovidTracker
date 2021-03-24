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

function getAge(dateString) {
    var today = new Date();
    var birthDate = new Date(dateString);
    var age = today.getFullYear() - birthDate.getFullYear();
    var m = today.getMonth() - birthDate.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
        age--;
    }
    return age;
}

function setValue(uid) {
	document.getElementById("submission").value = uid;
    var state = document.getElementById("state-select").value;
    var contact = Number(document.querySelector('input[name="contact"]:checked').value);

    // Fills result array with the selected option values
    var multi = document.getElementById("multi-select");

    var result = [];
    var options = multi && multi.options;
    var opt;

    for (var i = 0, iLen=options.length; i<iLen; i++) {
        opt = options[i];

        if (opt.selected) {
            result.push(opt.value  || opt.text);
        }
    }

    var userRef = db.collection('users').doc(uid);
    userRef.get().then((doc) => {
        var dob = doc.data().dob;
        console.log(dob)

        var smell_taste = result.includes("1");
        var fatigue = result.includes("2");
        var appetite = result.includes("3");
        var cough = result.includes("4");
        var compromised = result.includes("5");
        var vaccinated = result.includes("6");
        var age = getAge(dob);
    
        console.log(document.getElementById("submission").value);
        console.log(dob);
        console.log(age);
        console.log(state);
        console.log(contact);
        console.log(smell_taste);
        console.log(fatigue);
        console.log(appetite);
        console.log(cough);
        console.log(compromised);
        console.log(vaccinated);

        userRef.set({
            state: state,
            level_of_contact: contact,
            loss_of_smell_and_taste: smell_taste,
            severe_fatigue: fatigue,
            skipped_meals: appetite,
            persistent_cough: cough,
            immuno_compromised: compromised,
            vaccinated: vaccinated,
            age: age,
        }, { merge: true });
    }).catch((error) => {
        console.log("Error getting document:", error);
    })
}