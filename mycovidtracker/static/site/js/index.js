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
        riskAssessment.innerHTML = `${doc.data().risk_string}`
        riskAge.innerHTML = `You are ${doc.data().age} years old.`;
        if (doc.data().sex == true)
        {
            riskSex.innerHTML = `You are male.`
        }
        else
        {
            riskSex.innerHTML = `You are female.`
        }
        riskState.innerHTML = `You are heading to ${doc.data().state}.`
        if (doc.data().level_of_contact == 0)
        {
            riskLevel.innerHTML = `You intend to go to low risk areas.`
        }
        else if (doc.data().level_of_contact == 1)
        {
            riskLevel.innerHTML = `You intend to go to moderate risk areas.`
        }
        else
        {
            riskLevel.innerHTML = `You intend to go to high risk areas.`
        }
        if (doc.data().loss_of_smell_and_taste == true)
        {
            riskTaste.innerHTML = `You have loss of smell and taste.`
        }
        else
        {
            riskTaste.innerHTML = `You do not have loss of smell and taste.`
        }
        if (doc.data().severe_fatigue == true)
        {
            riskFatigue.innerHTML = `You are experiencing severe fatigue.`
        }
        else
        {
            riskFatigue.innerHTML = `You are not experiencing severe fatigue.`
        }
        if (doc.data().persistent_cough == true)
        {
            riskCough.innerHTML = `You have a persistent cough.`
        }
        else
        {
            riskCough.innerHTML = `You do not have a persistent cough.`
        }
        if (doc.data().immuno_compromised == true)
        {
            riskImmuno.innerHTML = `You are immunocompromised.`
        }
        else
        {
            riskImmuno.innerHTML = `You are not immunocompromised.`
        }
        if (doc.data().vaccinated == true)
        {
            riskVaccinated.innerHTML = `You have been vaccinated.`
        }
        else
        {
            riskVaccinated.innerHTML = `You have not been vaccinated.`
        }
        if (doc.data().skipped_meals == true)
        {
            riskAppetite.innerHTML = `You have loss of appetite.`
        }
        else
        {
            riskAppetite.innerHTML = `You do not have loss of appetite.`
        }

        document.getElementById("loader").style.display = 'none';
        document.getElementById("risk-container").style.display = 'block';
        
        document.getElementById("riskColor").style.backgroundColor = getColor(doc.data().risk_value);
        document.getElementById("gauge-fill").style.backgroundColor = getColor(doc.data().risk_value);
        
        const gaugeElement = document.querySelector(".gauge");
        setGaugeValue(gaugeElement, doc.data().risk_value);

        return doc.data().risk_value;
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
    }
        
}