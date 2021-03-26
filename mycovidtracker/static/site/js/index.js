const loggedOutLinks = document.querySelectorAll('.logged-out');
const loggedInLinks = document.querySelectorAll('.logged-in');

// hide/show UI elements for different login states
const setupUI = (user) => {
    if (user) {
        db.collection('users').doc(user.uid).get().then(doc => {
            details.innerHTML = `
              <div>
                <p>Email: ${doc.data().email}</p>
                <p>Age: ${doc.data().age}</p>
              </div>

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
    if (value.length > 2) {
        value = value.slice(0, 2);
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

function getColor(value){
    //value from 0 to 1
    var hue=((1-value)*120).toString(10);
    return ["hsl(",hue,",100%,50%)"].join("");
}

function setValue(uid) {
	document.getElementById("submission").value = uid;
    const state = document.getElementById("state-select").value;
    const contact = Number(document.querySelector('input[name="contact"]:checked').value);

    var userRef = db.collection('users').doc(uid);
    userRef.get().then((doc) => {

        const dob = doc.data().dob;
        const smell_taste = document.getElementById('1').checked;
        const fatigue = document.getElementById('2').checked;
        const appetite = document.getElementById('3').checked;
        const cough = document.getElementById('4').checked;
        const compromised = document.getElementById('5').checked;
        const vaccinated = document.getElementById('6').checked;
        const traveltime = Number(document.getElementById('travel-time').value);
        const age = getAge(dob);
    
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
            days_out: traveltime,
        }, { merge: true });
    }).catch((error) => {
        console.log("Error getting document:", error);
    })
}

function getRiskAssessment(uid) {
    db.collection('users').doc(uid).onSnapshot(doc => {
        setTimeout(() => {
            
        }, 1000);
        document.getElementById("risk-assessment").innerHTML = doc.data().risk_string;
        document.getElementById("loader").style.display = 'none';
        document.getElementById("risk-container").style.display = 'block';
        document.getElementById("risk-color").style.backgroundColor = getColor(doc.data().risk_value);
        document.getElementById("risk-color2").style.backgroundColor = getColor(doc.data().risk_value);
    });
}

function button(uid) {
    if (document.getElementById('state-select').value == "")
    {
        M.toast({html: 'Please select a state for Risk Assessment', displayLength: 1000});
    }
    else if (Number(document.getElementById('travel-time').value) > 30 || Number(document.getElementById('travel-time').value) < 1)
    {
        M.toast({html: 'Please enter a number from 1 to 30', displayLength: 1000});
    }
    else
    {
        setValue(uid);
        document.getElementById('loader').style.display='block';
        document.getElementById('risk-container').style.display='none';
        M.toast({html: 'Risk Factors sent. Please wait...', displayLength: 1000});
        getRiskAssessment(uid);
    }
        
}