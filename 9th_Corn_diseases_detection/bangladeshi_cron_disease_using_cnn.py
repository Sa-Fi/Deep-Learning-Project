# -*- coding: utf-8 -*-
"""Bangladeshi_cron_disease_using_CNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1c8b2poY_tBC5I5s1rusTgdkozwJwvmPR
"""

#upload the kaggle json
!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!kaggle datasets download -d nafishamoin/new-bangladeshi-crop-disease

# unzip the file 
import zipfile
zip_ref = zipfile.ZipFile('/content/new-bangladeshi-crop-disease.zip', 'r')
zip_ref.extractall('/content')
zip_ref.close()

!ls

#import all the necessary libraries
import os # for accessing the files 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg # visualize and process the image
import cv2 # open cv
from google.colab.patches import cv2_imshow # per cell e img show korar jnno within this window
from PIL import Image #read images and do some processes on it 
from sklearn.model_selection import train_test_split
import seaborn as sns
from glob import glob
import pandas as pd
import keras

# dataset_path = "/content/BangladeshiCrops/BangladeshiCrops/Crop___Disease/Corn"

# images = []
# labels = []
# counter = 1
# for label in os.listdir(dataset_path):
#     label_path = os.path.join(dataset_path, label)

#     for image_name in os.listdir(label_path):
#         image_path = os.path.join(label_path, image_name)
#         image = cv2.imread(image_path)
#         #image = cv2.resize(image,(256,256),interpolation=cv2.INTER_LINEAR)
#         images.append(image)
#         labels.append(label)
#         cv2_imshow(images)
#         if counter <= 3:
#           break

# print("total images ",len(images))
# print("total label ",len(labels))

# x = np.array(images)
# y = np.array(labels)
# print("type of x ",type(x))
# print("type of y ",type(y))

# plt.imshow(x[1100])
# plt.title(y[1100])

x = []
y = []

image_size = 224

labels = ['Corn___Common_Rust','Corn___Gray_Leaf_Spot','Corn___Healthy','Corn___Northern_Leaf_Blight']
counter = 1
for i in labels:
   folderPath = os.path.join('/content/BangladeshiCrops/BangladeshiCrops/Crop___Disease/Corn',i)
   for j in os.listdir(folderPath):
        img = cv2.imread(os.path.join(folderPath,j))
        img = cv2.resize(img,(image_size,image_size))
        x.append(img)
        y.append(i)

print('type, lenght, shape of the x',type(x),len(x),x[0].shape)
print('type, lenght, shape of the y',type(y),len(y),y)

x = np.array(x)
y = np.array(y)
print("type of x ",type(x))
print("type of y ",type(y))

plt.imshow(x[1])
plt.title(y[0])

# from keras.utils import to_categorical
# num_classes = len(np.unique(y))
# print('unique class of y',num_classes)
# # Convert the labels to categorical format
# y = to_categorical(y,num_classes=num_classes)
# y.shape

import numpy as np
from keras.utils import to_categorical

# Assuming you have the labels stored in a NumPy array 'y'

# Create a dictionary to map label strings to integer values
label_mapping = {
    'Corn___Common_Rust': 0,
    'Corn___Gray_Leaf_Spot': 1,
    'Corn___Healthy': 2,
    'Corn___Northern_Leaf_Blight': 3
}

# Map the label strings to integer values
y_mapped = np.array([label_mapping[label] for label in y])

# Get the number of classes
num_classes = len(label_mapping)

# Convert the labels to categorical format
y_categorical = to_categorical(y_mapped, num_classes=num_classes)

# Print the shape of the categorical labels
print('Shape of y_categorical:', y_categorical.shape)

x= x/255.0

y = y_categorical
# split the data
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.1,random_state = 101)

print("x shape ",x.shape)
print("x_train shape ",x_train.shape)
print("x_test shape ",x_test.shape)

print('y shape ',y.shape)
print("y_train shape ",y_train.shape)
print("y_test shape ",y_test.shape)

"""**Build the CNN model_1**"""

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense, BatchNormalization
from tensorflow.keras.optimizers import  RMSprop


# Define a sequential model
model = Sequential()

# Add convolutional layer with 32 filters, kernel size of (3,3), ReLU activation, and input shape
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(224,224,3)))
# Add max pooling layer with pool size of (2,2)
model.add(MaxPooling2D(pool_size=(2, 2)))                                                                                   # CONV BLOCK 1
# Add batch normalization layer
model.add(BatchNormalization())

# Add convolutional layer with 32 filters, kernel size of (3,3), ReLU activation
model.add(Conv2D(32, (3, 3), activation='relu'))
# Add max pooling layer with pool size of (2,2)
model.add(MaxPooling2D(pool_size=(2, 2)))
# Add batch normalization layer                                                                                               # CONV BLOCK 2
model.add(BatchNormalization())
# Add dropout layer with a rate of 0.5
model.add(Dropout(0.5))

# Add convolutional layer with 64 filters, kernel size of (3,3), ReLU activation
model.add(Conv2D(64, (3, 3), activation='relu'))
# Add batch normalization layer
model.add(BatchNormalization())
# Add max pooling layer with pool size of (2,2)                                                                              # CONV BLOCK 3
model.add(MaxPooling2D(pool_size=(2, 2)))
# Add dropout layer with a rate of 0.25
model.add(Dropout(0.25))

# Add flatten layer
model.add(Flatten())

# Add dense layer with 128 units and ReLU activation
model.add(Dense(128, activation='relu'))
# Add dropout layer with a rate of 0.5
model.add(Dropout(0.5))                                                                                                     # CLASSIFICATION HEAD
# Add dense layer with 2 units and softmax activation
model.add(Dense(4, activation='softmax')) 

# Define optimizer as RMSprop with learning rate of 0.0001
optimizer = RMSprop(learning_rate=0.0001)

# Compile model with categorical crossentropy loss and accuracy metric
model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

# Print model summary
model.summary()

history=model.fit(x_train,y_train,epochs = 20,validation_split =0.1)

loss, accuracy = model.evaluate(x_test, y_test)
print('Test Accuracy =', accuracy)
print('Loss =', loss)

h = history
#plot the accuracy value 
plt.plot(h.history['accuracy'],label='train accuracy')
plt.plot(h.history['val_accuracy'],label = 'validation accuracy')
plt.legend()
plt.show()

#plot the loss value 
plt.plot(h.history['loss'],label = 'train loss')
plt.plot(h.history['val_loss'],label = 'validation loss')
plt.legend()
plt.show()

input_image_path = input('Path of the image to be predicted: ')

input_image = cv2.imread(input_image_path)

cv2_imshow(input_image)

input_image_resized = cv2.resize(input_image, (224,224))

#input_image_scaled = input_image_resized/255

input_image_reshaped = np.reshape(input_image_resized, [1,224,224,3])

input_prediction = model.predict(input_image_reshaped)

print("Probability of Corn___Common_Rust,Corn___Gray_Leaf_Spot,Corn___Healthy,Corn___Northern_Leaf_Blight")
print(input_prediction)


input_pred_label = np.argmax(input_prediction)

print(input_pred_label)


if input_pred_label == 0:

  print('Corn___Common_Rust')

elif input_pred_label ==1:

  print('Corn___Gray_Leaf_Spot')
elif input_pred_label ==2:

  print('Corn___Healthy')

elif input_pred_label ==3:

  print('Corn___Northern_Leaf_Blight')

model.save('/content/drive/MyDrive/Deep learning Save model/Corn_diseases_detection.h5')

# labels = ['Corn___Common_Rust', 'Corn___Gray_Leaf_Spot', 'Corn___Healthy', 'Corn___Northern_Leaf_Blight']
# image_folder = '/content/BangladeshiCrops/BangladeshiCrops/Crop___Disease/Corn/Corn___Common_Rust'  # Replace with the actual path to your image folder
# target_size = (224, 224)

# images = []
# labels = []
# counter = 1
# for label in labels:
#     image_path = f"{image_folder}/{label}.jpg"  # Assuming the image filenames follow the label names with '.jpg' extension

#     # Read the image
#     image = cv2.imread(image_path)

#     # Resize the image
#     resized_image = cv2.resize(image, target_size)

#     images.append(resized_image)
#     labels.append(label)

#     cv2_imshow(label, resized_image)

#     if counter <=1:
#       break

# images = np.array(images)
# labels = np.array(labels)

len(images)

