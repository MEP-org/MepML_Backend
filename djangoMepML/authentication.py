import requests
import os
from dotenv import load_dotenv
load_dotenv()

FIREBASE_KEY = os.environ.get("firebase-key")

BASE_URL = "https://identitytoolkit.googleapis.com/v1/accounts:"

# register
def crate_new_pyromancer(email, password):
    
    details = {
        'email': email,
        'password': password,
        'returnSecureToken': True
    }
    
    r = requests.post(BASE_URL+"signUp?key=" + FIREBASE_KEY, data=details)
    print(r)
    print()
    print()

    return "error" in r.json(), r.json().get("localId")


# login
def fire_in(email, password):
    details = {
        'email': email,
        'password': password,
        'returnSecureToken': True
    }
    r = requests.post(BASE_URL + "signInWithPassword?key=" + FIREBASE_KEY, data=details)
    print(r)
    print()
    print()

    return "error" in r.json(), r.json().get("localId")
