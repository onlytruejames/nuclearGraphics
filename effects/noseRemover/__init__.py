from PIL import Image
from face_lib import face_lib
import random
import numpy as np
import math as maths

fl = face_lib()

def poprow(my_array,pr):
    """ row popping in numpy arrays
    Input: my_array - NumPy array, pr: row index to pop out
    Output: [new_array,popped_row] """
    i = pr
    pop = my_array[i]
    new_array = np.vstack((my_array[:i],my_array[i+1:]))
    return [new_array,pop]

def callback(image):
    shape = image.size
    open_cv_image = np.array(image.convert("RGB")) 
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    no_of_faces, noses = fl.faces_locations(open_cv_image)
    if no_of_faces:
        noses = [[nose[1] + 0.3 * nose[3], nose[1] + 0.65 * nose[3]] for nose in noses]
        image = np.array(image)
        gone = []
        for nose in noses:
            for n in range(int(nose[0]), int(nose[1]), 1):
                gone.append(n)
        for i in range(len(image[0])):
            it = len(image[0]) - i
            if it in gone:
                image, a = poprow(image, it)
        return Image.fromarray(image).resize(shape)
    return image