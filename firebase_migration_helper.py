# Firebase Content Migration Script
# This script helps you add existing static content to Firebase

import firebase_admin
from firebase_admin import credentials, firestore
import os

# Initialize Firebase (you'll need to add your service account key)
# cred = credentials.Certificate("path/to/your/serviceAccountKey.json")
# firebase_admin.initialize_app(cred)
# db = firestore.client()

def add_service_to_firebase(service_type, service_title, content):
    """Add a service to Firebase Firestore"""
    try:
        doc_ref = db.collection('services').document()
        doc_ref.set({
            'type': service_type,
            'title': service_title,
            'content': content
        })
        print(f"✅ Added to Firebase: {service_title} ({service_type})")
    except Exception as e:
        print(f"❌ Error adding {service_title}: {e}")

# Example usage:
# add_service_to_firebase("CA", "Start A Business", "<h2>Starting Your Business</h2><p>Content here...</p>")

print("📋 To migrate existing content to Firebase:")
print("1. Install firebase-admin: pip install firebase-admin")
print("2. Add your Firebase service account key")
print("3. Uncomment the Firebase initialization code")
print("4. Add your existing content using the add_service_to_firebase function")
print("5. Or use the admin panel at /admin/manage-services.html")
