

import json
from apps.home import blueprint
from flask import render_template, request, Response, flash, redirect, stream_with_context
from werkzeug.utils import secure_filename
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.firebasee import *
import os
from functions.parking_space import parking_space
from functions.counting_people import computePeople
from functions.gender_classification import classifyGender
from Live_demo_Shoplifting import Display, Receive
import cv2 as cv
from datetime import date, datetime


UPLOAD_FOLDER = 'apps/static/assets/uploads/'
newly_uploaded_file = ''
parking_path = ''


@blueprint.route('/index')
@login_required
def index():
    dt_object = datetime.fromtimestamp(datetime.timestamp(datetime.now()))
    date_object = datetime.fromtimestamp(datetime.timestamp(datetime.now()))
    labels, data = get_data_for_charts(str(dt_object.date()))
    dataCard = max(data) if len(data) != 0 else 0
    print('Max count is : ', dataCard)
    genderlabels, maledata = get_data_for_genderCharts(str(date_object.date()))
    print("Gender Data : " ,genderlabels, maledata)




    return render_template('home/index.html', segment='index', data = data, dataCard = dataCard, labels= labels, 
                                                                genderlabels = genderlabels, maledata = maledata)

 

def gen(cap):
    while True:
        frame = computePeople(cap)
        yield(b'--frame\r\n'
       b'Content-Type:  image/jpeg\r\n\r\n' + frame +
         b'\r\n\r\n')


def parkingGen(cap):
    while True:
        frame = parking_space(cap)
        yield(b'--frame\r\n'
       b'Content-Type:  image/jpeg\r\n\r\n' + frame +
         b'\r\n\r\n')


@blueprint.route('/people-count')
@login_required
def peopleCount():
    cap = cv.VideoCapture(newly_uploaded_file)
    return Response(gen(cap),
    mimetype='multipart/x-mixed-replace; boundary=frame')



@blueprint.route('/parking-space')
@login_required
def parkingSpace():
    cap = cv.VideoCapture(parking_path)
    return Response(parkingGen(cap),
    mimetype='multipart/x-mixed-replace; boundary=frame')


@blueprint.route('/people', methods=['GET', 'POST'])
@login_required
def people():
    global newly_uploaded_file
    if request.method == 'POST':
        if 'formFile' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['formFile']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            dest = os.path.join(UPLOAD_FOLDER, filename)
            newly_uploaded_file = dest

            file.save(dest)
            flash('File Uploaded!')
            return render_template("home/peopleCount.html", name=dest)

    return render_template('home/peopleCount.html', name='')


@blueprint.route('/parking', methods=['GET', 'POST'])
@login_required
def parking():
    
    global newly_uploaded_file, parking_path
    if request.method == 'POST':
        if 'formFile' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['formFile']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            dest = os.path.join(UPLOAD_FOLDER, filename)
            newly_uploaded_file = dest

            file.save(dest)
            parking_path = dest
            print(dest)
            flash('File Uploaded!')
            return render_template("home/ParkingSpace.html", name=dest)

    return render_template('home/ParkingSpace.html', name='')

def generate(cap):
    while True:
        frame = classifyGender(cap)
        if frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame +
                   b'\r\n')


def generateShoplifting(cap):
    Receive(cap)
    while True:
        frame = Display()
        if frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame +
                   b'\r\n')



@blueprint.route('/gender-classify')
@login_required
def Gender():
    cap = cv.VideoCapture(newly_uploaded_file)
    return Response(stream_with_context(generate(cap)),
    mimetype='multipart/x-mixed-replace; boundary=frame')


@blueprint.route('/gender', methods=['GET', 'POST'])
@login_required
def gender():
    global newly_uploaded_file
    if request.method == 'POST':
        if 'formFile' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['formFile']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            dest = os.path.join(UPLOAD_FOLDER, filename)
            newly_uploaded_file = dest
            file.save(dest)
            flash('File Uploaded!')
            return render_template("home/Gender.html", name=dest)
    return render_template('home/Gender.html', name='')

# @blueprint.route('/Gender', methods=['GET', 'POST'])
# @login_required
# def gender():
#     return render_template('home/Gender.html')

@blueprint.route('/shoplifting-fetch')
@login_required
def shoplifting_fetch():
    cap = cv.VideoCapture(newly_uploaded_file)
    return Response(stream_with_context(generateShoplifting(cap)),
    mimetype='multipart/x-mixed-replace; boundary=frame')


@blueprint.route('/shoplifting', methods=['GET', 'POST'])
@login_required
def detect_shoplifting():
    global newly_uploaded_file
    if request.method == 'POST':
        if 'formFile' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['formFile']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            dest = os.path.join(UPLOAD_FOLDER, filename)
            newly_uploaded_file = dest
            file.save(dest)
            flash('File Uploaded!')
            flash('Shoplifting Alert', 'error')
            return render_template("home/shoplifting.html", name=dest)
        
    return render_template('home/shoplifting.html', name='')


@blueprint.route('/get-shoplifting-data')
@login_required
def getShopliftingData():
    dt_object = datetime.now()
    date = str(dt_object.date())
    print(date)
    data = get_data_for_shoplifting(date)
    normal = get_data_for_shopliftingAlert(date)
    print("Table Data ",data)
    # win32api.MessageBox(0, 'Shoplifting detected please check your location', 'Shoplifting Alert')
    return render_template('home/show-shoplifting.html', data=data, normal=normal)


@blueprint.route('/get-data')
@login_required
def getData():
    users = get_data()
    print(users)

    dt_object = datetime.now()
    date = str(dt_object.date())    
    data = get_peoplecount_for_table(date)

    genderdata = get_gender_for_table(date)

    print("People Count Table Data ", data)
    return render_template('home/show.html', datas=users, data=data, genderdata=genderdata)

# @blueprint.route('/get-data')
# @login_required
# def getPeopleData():
#     data = get_data_for_charts()
#     print(data)
#     return render_template('home/show.html', data=data)


@blueprint.route('/play')
@login_required
def playVideo():

    return render_template('home/play.html')


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
