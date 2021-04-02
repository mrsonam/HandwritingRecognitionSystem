from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import tensorflow.keras as keras
import tensorflow as tf
import cv2
import glob
import os

os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'
model = tf.keras.models.load_model('C:/Users/sonam/OneDrive/Documents/HandwritingRecognitionSystem/register/best_model.h5')
class_mapping = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabdefghnqrt'
path = glob.glob("C:/Users/sonam/OneDrive/Documents/HandwritingRecognitionSystem/media/form/*.jpg")
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
    fn.append(class_mapping[np.argmax(model.predict(i))])
  print(fn)

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
  print(mn)

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

  print(ln)

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
  print(add)

  #Contact No.
  con1 = img.crop((202, 1262, 328, 1368))
  con2 = img.crop((332, 1262, 458, 1368))
  con3 = img.crop((462, 1262, 588, 1368))
  con4 = img.crop((592, 1262, 718, 1368))
  con5 = img.crop((722, 1262, 848, 1368))
  con6 = img.crop((852, 1262, 978, 1368))
  con7 = img.crop((982, 1262, 1108, 1368))
  con8 = img.crop((1112, 1262, 1238, 958))
  con9 = img.crop((1242, 1262, 1368, 958))
  con10 = img.crop((1372, 1262, 1498, 958))

  contact=[con1,con2,con3,con4,con5,con6,con7,con8,con9,con10]

  con=[]
  for x in contact:
    i = np.array(x)
    i = cv2.bitwise_not(i)
    i = cv2.resize(i, (28, 28))
    i = cv2.cvtColor(i, cv2.COLOR_RGB2GRAY)
    i = tf.keras.utils.normalize(i, axis=1)
    i = np.array(i).reshape(-1,28,28,1)
    con.append(class_mapping[np.argmax(model.predict(i))])
  print(con)