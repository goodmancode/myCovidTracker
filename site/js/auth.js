// retrieve data
/*db.collection*/

// change states w/ login status
auth.onAuthStateChanged(user => {
    if (user) {
        console.log('Current User: ', user);
        setupUI(user);
    } else {
        console.log('Not logged in');
        setupUI();
    }
})

// account creation
const signupForm = document.querySelector('#signup-form');
signupForm.addEventListener('submit', (e) => {
    e.preventDefault();

    // store input
    const email = signupForm['signup-email'].value;
    const password = signupForm['signup-password'].value;

    // ship to Firebase Auth
    auth.createUserWithEmailAndPassword(email, password).then(cred => {
        console.log(cred.user)
        const modal = document.querySelector('#modal-signup');
        // close form and reset fields after submission
        M.Modal.getInstance(modal).close();
        signupForm.reset();
        signupForm.querySelector('.helper-text').innerHTML = '';
    }).catch(function(error) {
        signupForm.querySelector('.helper-text').innerHTML = error.message;
      });
})

// sign out
const logout = document.querySelector('#logout');
logout.addEventListener('click', (e) => {
    e.preventDefault();
    auth.signOut();
})

// sign in 
const loginForm = document.querySelector('#login-form');
loginForm.addEventListener('submit', (e) => {
    e.preventDefault();

    // store input
    const email = loginForm['login-email'].value;
    const password = loginForm['login-password'].value;

    // ship to firebase auth
    auth.signInWithEmailAndPassword(email, password).then(cred => {
        const modal = document.querySelector('#modal-login');
        // close form and reset fields after submission
        M.Modal.getInstance(modal).close();
        loginForm.reset();
        loginForm.querySelector('.helper-text').innerHTML = '';
    }).catch(function(error) {
        loginForm.querySelector('.helper-text').innerHTML = error.message;
    });
})

// password reset
const resetForm = document.querySelector('#reset-form');
resetForm.addEventListener('submit', (e) => {
    e.preventDefault();

    // store input
    const email = resetForm['reset-email'].value;

    // ship to firebase auth
    auth.sendPasswordResetEmail(email).then(cred => {
        const modal = document.querySelector('#modal-reset');
        // close form and reset fields after submission
        M.Modal.getInstance(modal).close();
        resetForm.reset();
        // Email sent, alert user
        M.toast({html: 'Password Reset link sent to email'})
        resetForm.querySelector('.helper-text').innerHTML = '';
      }).catch(function(error) {
        resetForm.querySelector('.helper-text').innerHTML = error.message;
      });
})

// account deletion
const deleteForm = document.querySelector('#delete-form');
deleteForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const modal = document.querySelector('#modal-delete');
    const user = auth.currentUser;

    // store input
    const password = deleteForm['deletion-password'].value;

    // store credential from given username/password combo
    const credential = firebase.auth.EmailAuthProvider.credential(
        user.email, 
        password
    );

    // reauthenticate the user
    user.reauthenticateWithCredential(credential).then(function() {
        // User re-authenticated.
        M.Modal.getInstance(modal).close();
        deleteForm.reset();
        deleteForm.querySelector('.helper-text').innerHTML = '';

        // delete the user account
        auth.signOut();
        user.delete().then(function() {
            // User deleted.
            M.toast({html: 'Account deleted'})
            deleteForm.querySelector('.helper-text').innerHTML = '';
        }).catch(function(error) {
            // An error happened.
            deleteForm.querySelector('.helper-text').innerHTML = error.message;
        });

      }).catch(function(error) {
        // An error happened.
        deleteForm.querySelector('.helper-text').innerHTML = error.message;
      });
            
})
