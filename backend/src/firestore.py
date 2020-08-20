
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from src import params
from src.util import chunks

cred = credentials.ApplicationDefault()

firebase_admin.initialize_app(cred, {
  'projectId': params.GOOGLE_CLOUD_PROJECT,
})

db = firestore.client()

def insert_to_firestore(json_list,key_field,collection):
	
	for json_chunk in chunks(json_list,params.FIRESTORE_MAX):
		batch = db.batch()

		for json_item in json_chunk:
			doc_ref = db.collection(collection).document(json_item[key_field])
			batch.set(doc_ref, json_item, merge=True)

		# Commit the batch
		batch.commit()
