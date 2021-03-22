import firebase_admin
from firebase_admin import credentials, firestore, auth

def button(uid):
    # Use a service account
    cred = credentials.Certificate('/root/mycovidtracker/static/service.json')
    if not firebase_admin._apps:
	    firebase_admin.initialize_app(cred)
		
    db = firestore.client()

    doc_ref = db.collection(u'users').document(uid)
    doc_ref.set({
        u'username': u'functional',
        u'password': u'functional',
    }, merge=True)

