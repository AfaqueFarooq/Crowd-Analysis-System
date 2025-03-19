from firebase_admin import firestore
from firebase_admin import credentials
import firebase_admin
from datetime import datetime
from flask import session
# import win32api
import os
cred = credentials.Certificate("service-account-new.json")
firebase_admin.initialize_app(cred)

def get_db():
    database = firestore.client()
    return database

def get_data_for_charts(date):
    db = get_db()
    doc = db.collection('data').document(date)
    doc_data = doc.get().to_dict()
    labels, data = [], []
    if doc.get().exists:
        for entry in doc_data['entries']:
            labels.append(entry['time'])
            data.append(entry['count'])
    return labels, data

def get_peoplecount_for_table(date):
    db = get_db()
    doc = db.collection('data').document(date)
    doc_data = doc.get().to_dict()
    data = []
    if doc.get().exists:
        for index, entry in enumerate(doc_data['entries']):
            entry_with_index = {"index": index + 1, **entry}
            data.append(entry_with_index)
        # for entry in doc_data['entries']:
        #     data.append(entry)
    print('People Count Table Data : ',data)
    return data


def get_data_for_shopliftingAlert(date):
    db = get_db()
    doc = db.collection('shoplifting').document(date)
    doc_data = doc.get().to_dict()
    normal = []
    if doc.get().exists:
        for entry in doc_data['entries']:
            normal.append(entry['normal'])
    return normal

def get_data_for_shoplifting(date):
    db = get_db()
    doc = db.collection('shoplifting').document(date)
    doc_data = doc.get().to_dict()
    data = []
    if doc.get().exists:
        for index, entry in enumerate(doc_data['entries']):
            entry_with_index = {"index": index + 1, **entry}
            data.append(entry_with_index)
        # for entry in doc_data['entries']:
        #     data.append(entry)
    return data

def insert_shoplifting(bag, clothes, normal):
    print('Inserting Data')

    db = get_db()

    dt_object = datetime.now()

    doc = db.collection('shoplifting').document(str(dt_object.date()))

    if doc.get().exists:
        data = doc.get().to_dict()
        data['entries'].append({
            "bag":bag,
            "clothes":clothes,
            "normal":normal,
            "time": dt_object.strftime("%H:%M:%S")
            })
    else:
        data = {
            "entries": [
            {
            "bag":bag,
            "clothes":clothes,
            "normal":normal,
            "time": dt_object.strftime("%H:%M:%S")
            }
            ]
        }
    # if float(normal) < 0.50:
    #     generate_alert_message("Normal value is less than 0.50!", category='warning')

    doc.set(data)
    os.system("""osascript -e \'Shoplifting detected please check your location'""")
    # win32api.MessageBox(0, 'Shoplifting detected please check your location', 'Shoplifting Alert')
    print("inserted")

# def generate_alert_message(message, category='info'):
#     session['alert_message'] = message
#     session['alert_category'] = category

def insert_data_for_charts(timestamp, count):
    print('Inserting Data')
    db = get_db()
    dt_object = datetime.fromtimestamp(timestamp)

    doc = db.collection('data').document(str(dt_object.date()))

    if doc.get().exists:
        data = doc.get().to_dict()
        data['entries'].append({
            "count":count,
            "time": dt_object.strftime("%H:%M:%S")
            })
    else:
        data = {
            "entries": [
            {
            "count":count,
            "time": dt_object.strftime("%H:%M:%S")
            }
            ]
        }
    doc.set(data)

#insert_data_for_charts(datetime.timestamp(datetime.now()), 11)

def get_gender_for_table(date):
    db = get_db()
    doc = db.collection('genderData').document(date)
    doc_data = doc.get().to_dict()
    data = []
    if doc.get().exists:
        for index, entry in enumerate(doc_data['entries']):
            entry_with_index = {"index": index + 1, **entry}
            data.append(entry_with_index)
        # for entry in doc_data['entries']:
        #     data.append(entry)
    return data

def get_data_for_genderCharts(date):
    print("Getting Data")
    db = get_db()
    doc = db.collection('genderData').document(date)
    doc_data = doc.get().to_dict()
    genderlabels, maledata = [], [] 
    if doc.get().exists:
        for entry in doc_data['entries']:
            genderlabels.append(entry['time'])
            maledata.append(entry['male'])
            #femaledata.append(entry['female'])
            
        print("Gender Data : ",genderlabels, maledata)
    return genderlabels, maledata
    

def insert_data_for_genderCharts(timestamp, male, female):
    print('Inserting Data')
    db = get_db()
    date_object = datetime.fromtimestamp(timestamp)
    doc = db.collection('genderData').document(str(date_object.date()))

    if doc.get().exists:
        genderData = doc.get().to_dict()
        genderData['entries'].append({
            "male":male,
            "female":female,
            "time": date_object.strftime("%H:%M:%S")
            })
    else:
        genderData = {
            "entries": [
            {
            "male":male,
            "female":female ,
            "time": date_object.strftime("%H:%M:%S")           
            }
            ]
        }
    doc.set(genderData)




def insert_user(name, age, email):
    db = get_db()

    doc = db.collection('user').document()

    dictt = {
        "username":name,
        "age":age,
        "email":email,
        "id":doc.id
    }
    doc.set(dictt)

def get_data():

    db = get_db()
    docs = db.collection('user').stream()

    users = []
    for doc in docs:
        users.append(doc.to_dict())

    return users
    

