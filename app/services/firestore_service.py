import uuid
from firebase_admin import firestore
from app.core.config import db, bucket

class FirestoreService:

    def create_user(self, uid, email, role):
        db.collection("Users").document(uid).set({
            "email": email,
            "role": role,
            "created_at": firestore.SERVER_TIMESTAMP
        })

    def upload_file(self, file_bytes, filename, content_type):
        ext = filename.split('.')[-1]
        blob = bucket.blob(f"disaster_media/{uuid.uuid4()}.{ext}")
        blob.upload_from_string(file_bytes, content_type=content_type)
        blob.make_public()
        return blob.public_url

    def create_report(self, uid, media_url, disaster, severity):
        doc_ref = db.collection("Reports").add({
            "reporter_id": uid,
            "media_url": media_url,
            "disaster_type": disaster,
            "severity": severity,
            "status": "Pending",
            "created_at": firestore.SERVER_TIMESTAMP
        })
        return doc_ref[1].id

db_service = FirestoreService()