import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.ApplicationDefault()

app = firebase_admin.initialize_app(cred, {
  'projectId': os.getenv('APPLICATION_ID')
})

db = firestore.client(app)

def query_firestore(form_dict):

	col_ref = db.collection('item_data')

	print(form_dict)

	if form_dict['active_check'] == True and form_dict['sold_check'] == True:
		query = col_ref
	elif form_dict['active_check'] == False and form_dict['sold_check'] == False:
		query = col_ref.where('sold_status','==', "error")
	else:
		query = col_ref.where('sold_status','==', form_dict['sold_check'])
	
	if form_dict['date_selection']=='Last 1 day':
		query = query.where('last_1_day','==', True)
	elif form_dict['date_selection']=='Last 3 days':
		query = query.where('last_3_days','==', True)
	elif form_dict['date_selection']=='Last 7 days':
		query = query.where('last_7_days','==', True)
	else:
		query = query.where('all_time','==', True)

	query = query.where('price','>=', int(form_dict['minamount'])).where('price','<=', int(form_dict['maxamount']))

	
	if 'first_doc_id' not in form_dict or form_dict['first_doc_id']=='' or 'submit' in form_dict:
		query = query.order_by('price', direction=firestore.Query.DESCENDING).limit(10)
	else:
		if 'next_submit' in form_dict:
			print(form_dict['last_doc_id'])
			snapshot = col_ref.document(form_dict['last_doc_id']).get()
			query = query.order_by('price', direction=firestore.Query.DESCENDING).start_after(snapshot).limit(10)
		elif 'prev_submit' in form_dict:
			snapshot = col_ref.document(form_dict['first_doc_id']).get()
			query = query.order_by('price', direction=firestore.Query.DESCENDING).start_after(snapshot).limit_to_last(9)
	print(query.__dict__)
	fetched_results = query.get()

	
	if len(fetched_results)==10:
		end_query = False
	elif 'prev_submit' in form_dict:
		end_query = False
	else:
		end_query = True

	results = [doc.to_dict() for doc in fetched_results]
	
	return results[:9], end_query