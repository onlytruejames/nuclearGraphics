from PIL import Image
import numpy as np
from scipy.io.wavfile import read, write
import pyaudio

CHUNKSIZE = 50000

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=CHUNKSIZE)

def calc_closest_factors(c: int):
    if c//1 != c:
        raise TypeError("c must be an integer.")

    a, b, i = 1, c, 0
    while a < b:
        i += 1
        if c % i == 0:
            a = i
            b = c//a
    
    return (int(b), int(a), 4)

def wav2img(mode=1):
    data = stream.read(CHUNKSIZE)
    img = np.frombuffer(data, dtype=np.int16)
    if mode == 1:
        try:
            img = np.swapaxes(img, 0, 1)
            left, right = img[0], img[1]
        except:
            left, right = img, img
        shape = calc_closest_factors(len(left))
        img = np.array([
            (left // 256) + 128,
            (left % 256) + 128,
            (right // 256) + 128,
            (right % 256) + 128,
        ])
        img = np.swapaxes(img, 0, 1)
    else:
        img = np.floor_divide(img, 256)
        img += 128
        length = len(img)
        shape = calc_closest_factors(length)
        print(length)
        r = img[0:int(length * 0.25)]
        g = img[int(length * 0.25):int(length * 0.5)]
        b = img[int(length * 0.5):int(length * 0.75)]
        a = img[int(length * 0.75):length]
        img = np.hstack((r, g, b, a))
        print(img.shape)
        #img = np.swapaxes(img, 0, 1).astype(np.uint8)
        print(img.shape)
    return Image.fromarray(np.resize(img, shape).astype(np.uint8))

def variables(cam, clb):
    return []

def callback(img, variables):
    return wav2img()