
import os
from django.shortcuts import render
# import pyrebase

# cred = credentials.Certificate({
#  "type": "service_account",
#  "project_id": os.getenv('FIREBASE_PROJECT_ID'),
#  "private_key_id": os.environ.get('FIREBASE_PRIVATE_KEY_ID'),
#  "private_key": os.environ.get('FIREBASE_PRIVATE_KEY'),
#  "client_email": os.environ.get('FIREBASE_CLIENT_EMAIL'),
#  "client_id": os.environ.get('FIREBASE_CLIENT_ID'),
#  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#  "token_uri": "https://accounts.google.com/o/oauth2/token",
#  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#  "client_x509_cert_url": os.environ.get('FIREBASE_CLIENT_CERT_URL')
# })

# config = {
#     "apiKey": "AIzaSyDJx-fhJ8DZRv_b2KsZnuvKDfiwR6lCg5A",
#     "authDomain": "mepml-1ac7c.firebaseapp.com",
#     "projectId": "mepml-1ac7c",
#     "storageBucket": "mepml-1ac7c.appspot.com",
#     "messagingSenderId": "15756483554",
#     "appId": "1:15756483554:web:0419a622224710689af7bb",
#     "databaseURL": ""
# }

# firebase=pyrebase.initialize_app(config)
# authe = firebase.auth()

# def fire_in(request, email, password):
#     try:
#         user = authe.sign_in_with_email_and_password(email, password)
#     except:
#         return "Error", None
#     session_id = user['idToken']
#     request.session['uid'] = str(session_id)
#     return "Success", user['localId']


# def crate_new_pyromancer(email, password):
#     try:
#         user = authe.create_user_with_email_and_password(email, password)
#         uid = user['localId']
#     except:
#         return "Error", None
#     return "Success", uid