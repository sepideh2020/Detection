# USAGE
# Start the server:
# 	python main_server.py
# Submit a request via cURL:
# 	curl -X POST -F image=@dog.jpg 'http://localhost:5000/predict'
# Submita a request via Python:
#	python simple_request.py
#!/usr/bin/env python

# import the necessary packages
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from PIL import Image
import numpy as np
import flask
import io
import cv2

import os
from flask import Flask, abort, request, jsonify, g, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth

import json

from ml_services.affective_computing import FacialExpressionModel


from database.database import db
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from flask import g

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user



import sys
import os
import glob
import re
import numpy as np

# Keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer




import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np
from matplotlib.patches import Rectangle

def create_app():
    # initialization
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'   ###code kardan cookie eteghalesh be browser??
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://////home/sepideh/Desktop/detection/database.db'
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    bootstrap = Bootstrap(app)


    return app

app = create_app()


# extensions


db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
auth = HTTPBasicAuth()

def load_models():
	# load the pre-trained Keras model (here we are using a model
	# pre-trained on ImageNet and provided by Keras, but you can
	# substitute in your own networks just as easily)


	global model_affective
	model_affective = FacialExpressionModel("./models/model1.json", "./models/chkPt1.h5")



class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32),unique=True,index=True)
    password = db.Column(db.String(80))
31


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')   #karn nemikone

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)

                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)


@app.route('/api/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

@app.route('/api/dashboard')
@login_required
def dashboard():
    return render_template('indexpred.html', name=current_user.username)

@app.route('/api/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



#################################################################
#implementing api end points for authentication

@app.route('/api', methods=['GET'])
def server_status():
    return jsonify({'status': 'online'})


@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})



#################################################################
#implementing api end points


@app.route('/api/resource')             ###niyaze in a alan ba tavajoh be in ke lofin darim??/
@auth.login_required
def get_resource():
    # we can return some information about user here
    return jsonify({'data': 'Hello, %s!' % g.user.username})


@app.route("/detectfaces", methods=["POST"])
@auth.login_required
def detect_faces():
    # initialize the data dictionary that will be returned from the view
    data = {"success": False}

    if flask.request.method == "POST":
        if flask.request.files.get("image"):
            # read the image in PIL(Python Imaging Library) format
            image = flask.request.files["image"].read()
            image = Image.open(io.BytesIO(image))
            # convert pillow image to opencv for face detection
            image = np.array(image)

            # preprocess the image and prepare it for classification
            # image = prepare_image(image, target=(224, 224))


            #For color conversion, we use the function
            # cv2.cvtColor(input_image, flag) where flag determines the type of conversion.
            #For BGR to Gray conversion we use the flags cv2.COLOR_BGR2GRAY
            image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

            faces = model_affective.detect_faces(image)    ###alan mifahme bayad az file
                                                           ### affective_computing.py estefade kone?
            data['faces'] = json.dumps(faces.tolist())
            data["success"] = True
    return jsonify(data)

@app.route("/compare", methods=["POST"])
@auth.login_required           ###mige ghablesh tabe login bayad ejra beshe?
def compare():
    # initialize the data dictionary that will be returned from the view
    data = {"success": False}

    if flask.request.method == "POST":       ###chetor bayad piyade sazish konim baraye moghayese?
        if flask.request.files.get("image1") and flask.request.files.get("image2"):
            # read the image in PIL format
            image1 = flask.request.files["image1"].read()
            image1 = Image.open(io.BytesIO(image1))
            # convert pillow image to opencv for face detection
            image1 = np.array(image1)

            image2 = flask.request.files["image2"].read()
            image2 = Image.open(io.BytesIO(image2))
            # convert pillow image to opencv for face detection
            image2 = np.array(image2)

            # preprocess the image and prepare it for classification
            # image = prepare_image(image, target=(224, 224))
            #image1 = cv2.cvtColor(image1, cv2.COLOR_RGB2GRAY)


            faces = model_face_recognition.compare(image1, image2)  ###????
            data['faces'] = json.dumps(faces.tolist())

            data["success"] = True
    return jsonify(data)


@app.route("/detectemotion", methods=["POST"])
@auth.login_required
def detect_emotion():
	# initialize the data dictionary that will be returned from the view
	data = {"success": False}

	# ensure an image was properly uploaded to our endpoint
	if flask.request.method == "POST":
		if flask.request.files.get("image"):
			# read the image in PIL format
			image = flask.request.files["image"].read()
			image = Image.open(io.BytesIO(image))
			# convert pillow image to opencv for face detection
			image = np.array(image)

			# preprocess the image and prepare it for classification
			#image = prepare_image(image, target=(224, 224))
			image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

			emotions = model_affective.predict_all_faces_emotion(image)   ###az che fili mikhone?
			data['prediction'] = emotions
			data["success"] = True

	# return the da ta dictionary as a JSON response
	return flask.jsonify(data)







'''''@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['image']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        img = cv2.imread(file_path)
        # cv2.imshow('tt', img)
        # cv2.waitKey(2000)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        # Make prediction
        #preds = model_affective.predict_all_faces_emotion(file_path,model_affective)
        preds = model_affective.predict_all_faces_emotion(img)

        # Process your result for human
        # pred_class = preds.argmax(axis=-1)            # Simple argmax
        pred_class = decode_predictions(preds, top=1)   # ImageNet Decode
        result = str(pred_class[0][0][1])               # Convert to string
        return result
    return None '''

def double_quote(word):
    return '"%s"' % word

from PIL import Image
@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['image']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))
        f.save(file_path)
        img = cv2.imread(file_path)
        # print(img)
        print("AAA")
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        #predict=Image.open(img)
        # Make prediction
        preds, faces, all_types = model_affective.predict_all_faces_emotion(img)
        # print(all_types)
        img = cv2.imread(file_path)

        for (x,y,w,h) in faces:
            #fc = img[y:y + h, x:x + w]
            cv2.rectangle(img,(x,y),(x+w,y+h),(int(random.random() * 256), int(random.random() * 256),int(random.random() * 256)), 2)

        cv2.imwrite(file_path , img)

        a = file_path.split('/')
        stt =a[7]
        print(stt)
        retVal = []
        # all_types.append(stt)
        # returnVal = [stt, all_types[0]]
        all_types.append(stt)
        retVal = []

        retVal.append(len(all_types))
        for i in range(len(all_types)):
            retVal.append(str(all_types[i]))

        return str(retVal)




    return None



import random


# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
	print(("* Loading Keras model and Flask starting server..."
		"please wait until server has fully started"))

	load_models()

	if not os.path.exists('database.db'):
		db.create_all()


	app.run(debug =True)    ###az koja shoro mikone be run harkodomom seda function ie ro seda konim run mikone?

