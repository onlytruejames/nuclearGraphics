from PIL import Image
import numpy as np
from pykuwahara import kuwahara
from cv2 import cvtColor, COLOR_BGR2RGB, COLOR_RGB2BGR

def variables(cam, clb):
    return[]

def callback(img, variables):
    img = cvtColor(np.array(img), COLOR_RGB2BGR)
    img = kuwahara(img)
    return Image.fromarray(cvtColor(img, COLOR_BGR2RGB))