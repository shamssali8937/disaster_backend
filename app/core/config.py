import os
import firebase_admin
from firebase_admin import credentials, firestore, storage
from dotenv import load_dotenv

load_dotenv()

cred = credentials.Certificate("firebase-service-account.json")

firebase_admin.initialize_app(cred, {
    "storageBucket": os.getenv("FIREBASE_BUCKET")
})

db = firestore.client()
bucket = storage.bucket()