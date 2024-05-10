import cv2
import numpy as np
from PIL import Image

def callback(image):
    ## (1) Read
    img = np.array(image.convert("RGB")) 
    img = img[:, :, ::-1].copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ## (2) Threshold
    th, threshed = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)

    ## (3) Find the first contour that greate than 100, locate in centeral region
    ## Adjust the parameter when necessary
    cnts = cv2.findContours(threshed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
    cnts = sorted(cnts, key=cv2.contourArea)
    H,W = img.shape[:2]
    for cnt in cnts:
        x,y,w,h = cv2.boundingRect(cnt)
        if cv2.contourArea(cnt) > 100 and (0.7 < w/h < 1.3) and (W/4 < x + w//2 < W*3/4) and (H/4 < y + h//2 < H*3/4):
            break

    ## (4) Create mask and do bitwise-op
    mask = np.zeros(img.shape[:2],np.uint8)
    cv2.drawContours(mask, [cnt],-1, 255, -1)
    
    r = image.getchannel("R")
    g = image.getchannel("G")
    b = image.getchannel("B")
    return Image.merge("RGBA", (r, g, b, Image.fromarray(mask)))