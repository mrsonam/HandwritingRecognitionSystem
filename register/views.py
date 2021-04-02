from django.views.generic import View
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import date
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from.models import InputPic
import pyrebase
from .forms import ProfileUpdateForm, InputPicForm
import firebase_admin
from firebase_admin import auth as fb_auth
from firebase_admin import credentials
import re
from PIL import Image
import numpy as np
import tensorflow as tf
import cv2
import os 
import glob 
import random

#python-firebase configuration
cred = credentials.Certificate('json/firebase.json') 
default_app = firebase_admin.initialize_app(cred)

#pyrebase configuration
config = {
    'apiKey': "AIzaSyCTqdwvvKc7XbdkPQ9nE5JJR3YX6JFXL3s",
    'authDomain': "handwriting-recognition-system.firebaseapp.com",
    'projectId': "handwriting-recognition-system",
    'databaseURL' : "https://handwriting-recognition-system-default-rtdb.firebaseio.com",
    'storageBucket': "handwriting-recognition-system.appspot.com",
    'messagingSenderId': "976496926200",
    'appId': "1:976496926200:web:251267d753d5ea06a0ca0d",
    'measurementId': "G-X0BYRRH7S5"
}
firebase = pyrebase.initialize_app(config) #initializing firebase
firebase_auth = firebase.auth()
database = firebase.database()
storage = firebase.storage()

#regex
email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

#renders the index page
def index(request):
    return render(request, 'index.html')

#renders the registration page
def register(request):       
    return render(request, "register.html")

#renders the login page
def login(request):
    return render(request, 'login.html')

#gets the data filled by the user in the regitration page and fills the data in the database table if it is valid
def registration_form_submission(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if not (re.search(email_regex,email)):
            messages.error(request, f'Please enter a valid email address.')
            return redirect('register:register')

        exists = False
        try:
            exists = fb_auth.get_user_by_email(email)
            
        except:
            pass
            
        if exists:
            messages.error(request, f'This email address is already in use, please register using a different email address')
            return redirect('register:register')

        if len(password1) < 6:
            messages.error(request, f'Passwords should be atleast 6 characters long.')
            return redirect('register:register')

        if password1 != password2:
            messages.error(request, f'Your passwords do not match.')

        if password1 == password2: #checks if password1 and password2 matches
            user = firebase_auth.create_user_with_email_and_password(email, password1)
            
            if user is not None:
                #firebase_auth.sign_in_with_email_and_password(email,password1)
                uid = user['localId']
                data = {
                    "Name" : first_name + " " + last_name,
                    "Email" : email,
                    "profilePic" : "https://firebasestorage.googleapis.com/v0/b/handwriting-recognition-system.appspot.com/o/default.jpg?alt=media&token=9112ca11-4bcc-4100-ad2d-f15b952b8ae0"
                }
                database.child("Users").child(uid).set(data)
                firebase_auth.send_email_verification(user['idToken'])
                messages.success(request, f'Your account has been created! Please verify your email.')
                return redirect('register:login')

    return render(request, "register.html")

#gets the data filled by the user in the login page and fills the data in the database table if it is valid
def login_form_submission(request):
    email = request.POST['email']
    password = request.POST['password']

    if not (re.search(email_regex,email)):
        messages.error(request, f'Please enter a valid email address.')
        return redirect('register:login')

    try:
        verified = fb_auth.get_user_by_email(email)
            
    except:
        messages.error(request, f'Invalid username or password! \n\n Please use valid credentials.')
        return redirect('register:login')

    if verified.email_verified:
        try:
            user = firebase_auth.sign_in_with_email_and_password(email,password)
            # before the 1 hour expiry:
            user = auth.refresh(user['refreshToken'])
            # now we have a fresh token
            user['idToken']
                
        except:
            messages.error(request, f'Invalid username or password! \n\n Please use valid credentials.')
            return redirect('register:login')
    
    else:
        messages.error(request, f'Please verify your email before you log in')
        return redirect('register:login')

    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    return redirect('register:welcome')

#renders the forgot password page
def reset_password(request):
    return render(request, 'reset_password.html')

#sends email to reset the password of the user
def reset_password_sent(request):
    email = ""
    if request.method == 'POST':
        email = request.POST.get('email')
    if email is not None:
        try:
            firebase_auth.send_password_reset_email(email)
            return render(request, 'reset_password_sent.html')
        except:
            messages.error(request, f'Please enter a valid email address.')
            return render(request, 'reset_password.html')

    return render(request, 'reset_password.html')

#this page renders the welcome page
def welcome(request):
    profilePic = get_profilePic(request)
    name = get_name(request)
    if request.method == "POST": 
        i_form = InputPicForm(request.POST, request.FILES)
        imageURL = None

        if i_form.is_valid():
            try:
                imageURL = i_form.cleaned_data['image']
                obj = InputPic.objects.create(
                                 image = imageURL
                                 )
                obj.save()
            
            except :
                messages.error(request, f'Error')
                
            stringAll = crop()
            data = {
                'f_name' : stringAll[0],
                'm_name' : stringAll[1],
                'l_name' : stringAll[2],
                'address' : stringAll[3],
                'profilePic' : profilePic,
                'name' : name,
            }
            # with open('C:/Users/sonam/OneDrive/Documents/HandwritingRecognitionSystem/register/DataOutput.csv','a+') as f:
            #     for stringData in stringAll:
            #         f.write(stringData+',')
            #     f.write('\n')
            return render(request, 'add_student.html', data)

    else:
        i_form = InputPicForm()
    context = {
        'i_form': i_form,
        'profilePic' : profilePic,
        'name' : name,
    }
    return render(request, 'welcome.html', context)

#renders the settings page
def settings(request):
    profilePic = get_profilePic(request)
    name = get_name(request)      
    return render(request, "settings.html", {"profilePic" : profilePic, "name" : name})

#renders the changePP page
def change_PP(request):
    name = get_name(request)
    idtoken = request.session['uid']
    a = firebase_auth.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    profilePic = database.child("Users").child(a).child('profilePic').get().val()
    
    if request.method == "POST": 
        p_form = ProfileUpdateForm(request.POST, request.FILES)
        imageURL = None

        if p_form.is_valid():
            imageURL = p_form.cleaned_data['image']
            try:
                p_form.save()
            
            except :
                messages.error(request, f'Error')

            storage.child("/profile_pic").child(str(imageURL)).put(imageURL)
            updatedProfilePic = storage.child("/profile_pic").child(str(imageURL)).get_url(a)
            database.child("Users").child(a).update({'profilePic': str(updatedProfilePic)})
            profilePic = database.child("Users").child(a).child('profilePic').get().val()
            messages.success(request, f'Your Profile Picture has been updated')
            return render(request, "change_PP.html", {'p_form': p_form,'profilePic' : profilePic})
        
    else:
        p_form = ProfileUpdateForm()
    context = {
        'p_form': p_form,
        'profilePic' : profilePic,
        'name' : name
    }

    return render(request, "change_PP.html", context)

#renders the change password page
def change_password(request):
    profilePic = get_profilePic(request)
    name = get_name(request)
    email = get_email(request)
    return render(request, 'change_password.html', {"email": email, "profilePic": profilePic, "name" : name})

#sends email to reset the password of the user
def change_password_sent(request):
    profilePic = get_profilePic(request)
    name = get_name(request)
    email = get_email(request)

    if email is not None:
        firebase_auth.send_password_reset_email(email)
        messages.success(request, f'An email has been sent to your email address. Please follow the link in the email to change your password')
        return render(request, 'change_password.html', {"profilePic" : profilePic, "name" : name})

    return render(request, 'change_password.html', {"profilePic" : profilePic, "name" : name})

#renders the add student page
def add_student(request):
    profilePic = get_profilePic(request)
    name = get_name(request)
    context = {'profilePic' : profilePic,
                'name' : name
    }     
    return render(request, "add_student.html", context)

#gets the data filled by the user in the add student page and fills the data in the database table if it is valid
def student_form_submission(request):
    f_name = request.POST['f_name']
    m_name = request.POST['m_name']
    l_name = request.POST['l_name']
    address = request.POST['address']

    data = {
            "Name" : f_name + " " + m_name + " " + l_name,
            "Address" : address          
    }
    database.child("Students").child(random.randint(0,1000)).set(data)
    messages.success(request, f'The student has been added succesfully')
    return redirect('register:welcome')

#renders the student info page
def student_info(request):
    profilePic = get_profilePic(request)
    name = get_name(request)
    students = get_studentInfo()
    
    context = {'profilePic' : profilePic,
                'name' : name,
                'students' : students,
    }
    return render(request, "student_info.html", context)

#logs the user out from the system
def logout(request):
    try:
        del request.session['uid']
    except:
        pass
    return redirect('register:login')

#renders the privacy policy page
def privacy_policy(request):       
    return render(request, "privacy_policy.html")

#renders the terms and conditions page
def terms_conditions(request):       
    return render(request, "terms_conditions.html")

#returns path of the profile pic
def get_profilePic(request):
    idtoken = request.session['uid'] #fetching uid through token
    a = firebase_auth.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    profilePic = database.child("Users").child(a).child('profilePic').get().val()
    return profilePic

#returns student info
def get_studentInfo():
    ids = database.child("Students").get()
    infos=[]
    for id in ids.each():
        info=[]
        x = id.key()
        name = database.child("Students").child(x).child('Name').get().val()
        address = database.child("Students").child(x).child('Address').get().val()
        info.append(x)
        info.append(name)
        info.append(address)
        infos.append(info)
        
    return infos

#returns email of the user
def get_email(request):
    idtoken = request.session['uid']
    a = firebase_auth.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    email = database.child("Users").child(a).child('Email').get().val()
    return email

#returns name of the user
def get_name(request):
    idtoken = request.session['uid']
    a = firebase_auth.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    name = database.child("Users").child(a).child('Name').get().val()
    return name

#crops the image into sections and predicts the character
def crop():
    os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'
    model = tf.keras.models.load_model('C:/Users/sonam/OneDrive/Documents/HandwritingRecognitionSystem/register/model.h5')
    class_mapping = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabdefghnqrt'
    
    path = glob.glob("C:/Users/sonam/OneDrive/Documents/HandwritingRecognitionSystem/media/form/*.jpg")
    all = []
    stringAll = []
    for file in path:
        img = Image.open(file)

        fn1 = img.crop((202, 442, 328, 548))
        fn2 = img.crop((332, 442, 458, 548))
        fn3 = img.crop((462, 442, 588, 548))
        fn4 = img.crop((592, 442, 748, 548))
        fn5 = img.crop((722, 442, 848, 548))
        fn6 = img.crop((852, 442, 978, 548))
        fn7 = img.crop((982, 442, 1108, 548))
        fn8 = img.crop((1112, 442, 1238, 548))
        fn9 = img.crop((1242, 442, 1368, 548))
        fn10 = img.crop((1372, 442, 1498, 548))

        first_name=[fn1,fn2,fn3,fn4,fn5,fn6,fn7,fn8,fn9,fn10]

        fn=[]
        for x in first_name:
            i = np.array(x)
            i = cv2.bitwise_not(i)
            i = cv2.resize(i, (28, 28))
            i = cv2.cvtColor(i, cv2.COLOR_RGB2GRAY)
            i = tf.keras.utils.normalize(i, axis=1)
            i = np.array(i).reshape(-1,28,28,1)
            j = np.argmax(model.predict(i))
            fn.append(class_mapping[j])

        for x in range(0,len(fn)):
            if 'L' in fn:
                fn.remove('L')
        all.append(fn)

        #Middle Name
        mn1 = img.crop((202, 646, 328, 752))
        mn2 = img.crop((332, 646, 458, 752))
        mn3 = img.crop((462, 646, 588, 752))
        mn4 = img.crop((592, 646, 718, 752))
        mn5 = img.crop((722, 646, 848, 752))
        mn6 = img.crop((852, 646, 978, 752))
        mn7 = img.crop((982, 646, 1108, 752))
        mn8 = img.crop((1112, 646, 1238, 752))
        mn9 = img.crop((1242, 646, 1368, 752))
        mn10 = img.crop((1372, 646, 1498, 752))


        middle_name=[mn1,mn2,mn3,mn4,mn5,mn6,mn7,mn8,mn9,mn10]

        mn=[]
        for x in middle_name:
            i = np.array(x)
            i = cv2.bitwise_not(i)
            i = cv2.resize(i, (28, 28))
            i = cv2.cvtColor(i, cv2.COLOR_RGB2GRAY)
            i = tf.keras.utils.normalize(i, axis=1)
            i = np.array(i).reshape(-1,28,28,1)
            mn.append(class_mapping[np.argmax(model.predict(i))])

        for x in range(0,len(mn)):
            if 'L' in mn:
                mn.remove('L')
        all.append(mn)

        #Last Name
        ln1 = img.crop((202, 852, 328, 958))
        ln2 = img.crop((332, 852, 458, 958))
        ln3 = img.crop((462, 852, 588, 958))
        ln4 = img.crop((592, 852, 718, 958))
        ln5 = img.crop((722, 852, 848, 958))
        ln6 = img.crop((852, 852, 978, 958))
        ln7 = img.crop((982, 852, 1108, 958))
        ln8 = img.crop((1112, 852, 1238, 958))
        ln9 = img.crop((1242, 852, 1368, 958))
        ln10 = img.crop((1372, 852, 1498, 958))

        last_name=[ln1,ln2,ln3,ln4,ln5,ln6,ln7,ln8,ln9,ln10]

        ln=[]
        for x in last_name:
            i = np.array(x)
            i = cv2.bitwise_not(i)
            i = cv2.resize(i, (28, 28))
            i = cv2.cvtColor(i, cv2.COLOR_RGB2GRAY)
            i = tf.keras.utils.normalize(i, axis=1)
            i = np.array(i).reshape(-1,28,28,1)
            ln.append(class_mapping[np.argmax(model.predict(i))])

        for x in range(0,len(ln)):
            if 'L' in ln:
                ln.remove('L')
        all.append(ln)

        #Address
        add1 = img.crop((202, 1056, 328, 1162))
        add2 = img.crop((332, 1056, 458, 1162))
        add3 = img.crop((462, 1056, 588, 1162))
        add4 = img.crop((592, 1056, 718, 1162))
        add5 = img.crop((722, 1056, 848, 1162))
        add6 = img.crop((852, 1056, 978, 1162))
        add7 = img.crop((982, 1056, 1108, 1162))
        add8 = img.crop((1112, 1056, 1238, 1162))
        add9 = img.crop((1242, 1056, 1368, 1162))
        add10 = img.crop((1372, 1056, 1498, 1162))

        address=[add1,add2,add3,add4,add5,add6,add7,add8,add9,add10]

        add=[]
        for x in address:
            i = np.array(x)
            i = cv2.bitwise_not(i)
            i = cv2.resize(i, (28, 28))
            i = cv2.cvtColor(i, cv2.COLOR_RGB2GRAY)
            i = tf.keras.utils.normalize(i, axis=1)
            i = np.array(i).reshape(-1,28,28,1)
            add.append(class_mapping[np.argmax(model.predict(i))])
        for x in range(0,len(add)):
            if 'L' in add:
                add.remove('L')
        all.append(add)

        #Contact No.
        # con1 = img.crop((202, 1262, 328, 1368))
        # con2 = img.crop((332, 1262, 458, 1368))
        # con3 = img.crop((462, 1262, 588, 1368))
        # con4 = img.crop((592, 1262, 718, 1368))
        # con5 = img.crop((722, 1262, 848, 1368))
        # con6 = img.crop((852, 1262, 978, 1368))
        # con7 = img.crop((982, 1262, 1108, 1368))
        # con8 = img.crop((1112, 1262, 1238, 958))
        # con9 = img.crop((1242, 1262, 1368, 958))
        # con10 = img.crop((1372, 1262, 1498, 958))

        # contact=[con1,con2,con3,con4,con5,con6,con7,con8,con9,con10]

        # con=[]
        # for x in contact:
        #     i = np.array(x)
        #     i = cv2.bitwise_not(i)
        #     i = cv2.resize(i, (28, 28))
        #     i = cv2.cvtColor(i, cv2.COLOR_RGB2GRAY)
        #     i = tf.keras.utils.normalize(i, axis=1)
        #     i = np.array(i).reshape(-1,28,28,1)
        #     con.append(class_mapping[np.argmax(model.predict(i))])
        # all.append(con)
        for data in all:
            # for x in range(0,len(data)):
            #     if 'L' in data:
            #         data.remove('L')
            stringData = ''.join(map(str, data))
            stringAll.append(stringData)
        os.remove(file)
        return stringAll
