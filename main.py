print("If you are running this for the first time, run:")
print("sudo apt install python3-tk (if on Linux, for mac or pc look up how to install tkinter)")
print("pip install opencv-python")
print("pip install PIL")
print("pip install scikit-image")
print("pip install face-library")
print("pip install pykuwahara")
print("pip install mido")
print("pip install python-rtmidi")
import json, tkinter
import ascii, blurDart, rgbSwapper, mirrorEcho, colourOffset, imgFX, flipDiff, kaleidoscope, reciprocal, circle, maximum, oppDiff, pixSort, stretch, faceOnly, dissolve, kuwahara, palette, dogBlur, zoom, colourExpander, dogShift, fractalNoise, fromMic
from PIL import Image, ImageTk
from cv2 import VideoCapture, cvtColor, COLOR_BGR2RGB

import mido, rtmidi

callbacks = {
    "ascii": ascii,
    "blurDart": blurDart,
    "RGBSwapper": rgbSwapper,
    "mirrorEcho": mirrorEcho,
    "colourOffset": colourOffset,
    "imgFX": imgFX,
    "flipDiff": flipDiff,
    "kaleidoscope": kaleidoscope,
    "reciprocal": reciprocal,
    "circle": circle,
    "maximum": maximum,
    "oppDiff": oppDiff,
    "pixSort": pixSort,
    "stretch": stretch,
    "faceOnly": faceOnly,
    "dissolve": dissolve,
    "kuwahara": kuwahara,
    "palette": palette,
    "dogBlur": dogBlur,
    "zoom": zoom,
    "colourExpander": colourExpander,
    "dogShift": dogShift,
    "fractalNoise": fractalNoise,
    "fromMic": fromMic
}

global currentCallback, clb, currentFrame
clb = -1
currentFrame = 0

set = json.load(open("set.json", "r"))
isMidi = set["midi"]
if isMidi:
    i = 0
    done = False
    midiPorts = []
    try:
        x = rtmidi.MidiIn(0)
    except:
        pass
    x = rtmidi.MidiIn(0)
    while not done:
        try:
            midiPorts.append(x.get_port_name(i))
            i += 1
        except:
            done = True
    done = False
    if len(midiPorts) > 1:
        while not done:
            midiPort = int(input(f"Choose a midi port from this list. Give the index:\n{midiPorts}"))
            if 0 <= midiPort < len(midiPorts):
                done = True
            else:
                print("Invalid port")
    elif len(midiPorts) == 1:
        midiPort = 0
    else:
        print("MIDI is unavailable, please plug a controller in or create a virtual input.")
        isMidi = False
    if isMidi:
        midiIn = mido.open_input(midiPorts[midiPort])
midiOn = False
sequence = set["sequence"]

ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

class fakeCam:
    def __init__(self, port):
        self.cam = VideoCapture(port)
    def get(self, x):
        return int(self.cam.get(x))
    def read(self):
        global currentFrame, currentGif, frameNum
        currentFrame += 1
        try:
            if currentFrame >= frameNum - 1:
                currentFrame = 0
            currentGif.seek(currentFrame)
            frame = currentGif.copy().convert("RGB").resize((width, height))
            if currentCallback["gifAmount"] == 1:
                return True, frame
            result, image = self.getCam()
            if not result:
                return False, frame
            image = cvtColor(image, COLOR_BGR2RGB)
            image = Image.fromarray(image)
            return True, Image.blend(image, frame, currentCallback["gifAmount"])
        except:
            result, image = self.getCam()
            if not result:
                return False, None
            image = cvtColor(image, COLOR_BGR2RGB)
            image = Image.fromarray(image)
            return True, image
    def getCam(self):
        result, image = self.cam.read()
        if not result:
            return False, None
        return True, image

def list_ports():
    #stolen from stackoverflow
    nonWorkingPorts = []
    devPort = 0
    workingPorts = []
    while not len(nonWorkingPorts):
        camera = VideoCapture(devPort)
        if camera.isOpened():
            isReading, img = camera.read()
            if isReading:
                workingPorts.append(devPort)
            else:
                nonWorkingPorts.append(devPort)
        else:
            nonWorkingPorts.append(devPort)
        devPort +=1
    return workingPorts

ports = list_ports()

if len(ports) == 0:
    print("No camera ports are available, try plugging in a camera and try again")
    port = False

elif len(ports) == 1:
    port = 0

else:
    done = False
    while not done:
        port = int(input(f"Choose a camera port from this list: {ports}"))
        if port in ports:
            done = True
        else:
            print("Invalid port")

def callback(e):
    root.bind("<Button-1>", nextCallback)
    nextCallback(e)
    while True:
        msg = midiIn.poll()
        if msg:
            if msg.type == "note_on":
                nextCallback(e)
        try:
            result, image = cam.read()
            if result:
                for cb in currentCallback['names']:
                    image = callbacks[cb].callback(image, variables[cb])
                winWidth = root.winfo_width()
                winHeight = root.winfo_height()
                if winWidth / width > winHeight / height:
                    resize = winHeight / height
                else:
                    resize = winWidth / width
                img = image.resize((
                    int(width * resize),
                    int(height * resize)
                ))
                img = ImageTk.PhotoImage(img)
                label.configure(image = img)
                label.image = img
                root.update()
        except Exception as e:
            root.quit()
            raise e

def changeCallback():
    global currentCallback, clb, root, currentGif, currentFrame, frameNum
    frameNum = frameNums[clb]
    currentFrame = 0
    currentGif = gifs[clb]
    currentCallback = sequence[clb]
    modes = currentCallback['names']
    for mode in modes:
        variables[mode] = callbacks[mode].variables(cam, clb)
    #root.title(f"{currentCallback['names'][0].upper()}{currentCallback['names'][1:]}")

def nextCallback(e):
    global clb
    clb += 1
    clb = clb % len(sequence)
    changeCallback()

def prevCallback(e):
    global clb
    if clb == 0:
        clb = len(sequence)
    clb -= 1
    changeCallback()

if type(port) == int:
    global cam, root, frames
    cam = fakeCam(port)
    width = int(cam.get(3))
    height = int(cam.get(4))

    variables = {}

    for cb in callbacks.keys():
        variables[cb] = []

    gifs = []
    frameNums = []

    for event in range(len(sequence)):
        try:
            if sequence[event]["gifAmount"] > 0:
                gifs.append(Image.open(f"gifs/{event}.gif"))
                theGif = gifs[-0]
                num = 0
                while True:
                    try:
                        theGif.seek(num + 1)
                        num += 1
                    except:
                        break
                frameNums.append(num)
            else:
                gifs.append(False)
                frameNums.append(1)
        except:
            gifs.append(False)
            frameNums.append(1)

    root = tkinter.Tk()

    root.geometry("750x600")
    root.title("NuclearGraphics")

    img1 = ImageTk.PhotoImage(Image.open("nuclearGraphics.png"))

    label = tkinter.Label(root, image = img1, borderwidth=0, highlightthickness=0)
    label.pack()

    root.bind("<Right>", nextCallback)
    root.bind("<Left>", prevCallback)
    root.bind("<Return>", callback)
    root.mainloop()