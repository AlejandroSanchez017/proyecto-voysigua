import firebase_admin
from firebase_admin import credentials, auth, firestore
import os

# Obtener la ruta absoluta del archivo JSON de credenciales
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Ruta del directorio donde está este archivo
cred_path = os.path.join(BASE_DIR, "firebaseServiceAccount.json")  # Archivo de credenciales

# Verificar si Firebase ya está inicializado
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)  # Usa la ruta absoluta
    firebase_admin.initialize_app(cred)

# Inicializar Firestore
db = firestore.client()

print("Firebase inicializado correctamente.")

