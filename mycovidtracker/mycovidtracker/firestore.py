import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('service.json')
firebase_admin.initialize_app(cred)
uid = firebase.auth().currentUser.uid
print(uid)
db = firestore.client()

doc_ref = db.collection(u'users').document(u'taken@example.com')
doc_ref.set({
    u'username': u'random_name',
    u'password': u'random_password',
})
