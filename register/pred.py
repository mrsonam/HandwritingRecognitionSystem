from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import tensorflow.keras as keras
import tensorflow as tf
import cv2

img = Image.open(r"C:/Users/sonam/OneDrive/Documents/HandwritingRecognitionSystem/media/input_images/Filled-1.jpg")
fn1 = img.crop((200, 438, 330, 550))
fn2 = img.crop((330, 438, 460, 550))
fn3 = img.crop((460, 438, 590, 550))
fn4 = img.crop((590, 438, 720, 550))
fn5 = img.crop((720, 438, 850, 550))
fn6 = img.crop((850, 438, 980, 550))
fn7 = img.crop((980, 438, 1110, 550))
fn8 = img.crop((1110, 438, 1240, 550))
fn9 = img.crop((1240, 438, 1370, 550))
fn10 = img.crop((1370, 438, 1500, 550))

first_name=[fn1,fn2,fn3,fn4,fn5,fn6,fn7,fn8,fn9,fn10]

fn=[]
for x in first_name:
  img = np.array(x)
  img = cv2.bitwise_not(img)
  img = cv2.resize(img, (28, 28))
  #img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
  img = tf.keras.utils.normalize(img, axis=1)
  img = np.array(img).reshape(-1,28,28,1)

model = tf.keras.models.load_model('best_model.h5')

pred=[]
for x in fn:
  a = model.predict(x)
  pred.append(a)
  print("####################")
  print(np.argmax(a))
  print("####################")