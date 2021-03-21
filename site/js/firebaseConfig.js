// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
var firebaseConfig = {
	apiKey: "AIzaSyAYai5jWjOJbY5xfc_-19l0VJV_-sTHfV8",
	authDomain: "mycovidtracker-5e186.firebaseapp.com",
	projectId: "mycovidtracker-5e186",
	storageBucket: "mycovidtracker-5e186.appspot.com",
	messagingSenderId: "533040907274",
	appId: "1:533040907274:web:53eed874a3b4f384e48bf3",
	measurementId: "G-HCX4H5GSRT"
};
// Initialize Firebase
firebase.initializeApp(firebaseConfig);
firebase.analytics();
// Make references for auth and firestore
const auth = firebase.auth();
const db = firebase.firestore();
const storage = firebase.storage();
// update firestore config
//db.settings({ timestampsInSnapshots: true });