# detection
install the requirements by  pip install requirements.txt 

run it by python main_server.py

In this project I tried to develop a web server using Flask in which you can create an account for yourself, upload your photos and it will detect faces in the photo and predict the emotion of faces, it is able to detect upto four faces in the image.
I developed the detection part by using Neural Networks Classifiers. haarcascade_frontalface_deafult.xml for face detection and chkPt1.h5 model and a json model for emotion detection  in which you can find them in models folder which exists in the project folder 

At first new user should create an account for him or herself.
If the user already exists you will see the message “User already exists”. After creating an account for yourself you have to go to the login page.

After creating an account you should go to the login page.

Now you are able to upload your photos for predicting emotions in the image.

After uploading your photo “Predict!” button will be appeared.

And finally by pushing the Predict! button you can see what are the emotion of faces in the image and also see the percentage of each emotion that the model would predict in a chart.
For drawing bar chart I used Chart.js which is an open source JavaScript library on Github that allows you to draw different types of charts by using the HTML5 canvas element. 

The model which used for emotion detection is not very accurate and sometimes cannot recognize some faces in photos.


The other problem of this model is that sometimes does not predict emotions correctly.
