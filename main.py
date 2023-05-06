import json, tkinter
import liveAscii, liveBlurDart, liveRGBSwapper, liveMirrorEcho, liveColourOffset, liveImgFX, liveFlipDiff, liveKaleidoscope, liveReciprocal, liveCircle, liveMaximum, liveOppDiff, livePixSort, liveStretch
from PIL import Image, ImageTk
from cv2 import VideoCapture, cvtColor, COLOR_BGR2RGB

callbacks = {
    "ascii": liveAscii,
    "blurDart": liveBlurDart,
    "RGBSwapper": liveRGBSwapper,
    "mirrorEcho": liveMirrorEcho,
    "colourOffset": liveColourOffset,
    "imgFX": liveImgFX,
    "flipDiff": liveFlipDiff,
    "kaleidoscope": liveKaleidoscope,
    "reciprocal": liveReciprocal,
    "circle": liveCircle,
    "maximum": liveMaximum,
    "oppDiff": liveOppDiff,
    "pixSort": livePixSort,
    "stretch": liveStretch
}

global currentCallback, clb
clb = -1

global currentFrame
currentFrame = 0

sequence = json.load(open("set.json", "r"))

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
            result, image = self.cam.read()
            if not result:
                return False, frame
            image = cvtColor(image, COLOR_BGR2RGB)
            image = Image.fromarray(image)
            return True, Image.blend(image, frame, currentCallback["gifAmount"])
        except:
            result, image = self.cam.read()
            if not result:
                return False, None
            image = cvtColor(image, COLOR_BGR2RGB)
            image = Image.fromarray(image)
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
        try:
            img = callbacks[currentCallback['name']].callback(cam, variables[currentCallback['name']])
            winWidth = root.winfo_width()
            winHeight = root.winfo_height()
            if winWidth / width > winHeight / height:
                resize = winHeight / height
            else:
                resize = winWidth / width
            img = img.resize((
                int(width * resize),
                int(height * resize)
            ))
            img = ImageTk.PhotoImage(img)
            label.configure(image = img)
            label.image = img
            root.update()
        except Exception as e:
            raise e

def changeCallback():
    global currentCallback, clb, root, currentGif, currentFrame, frameNum
    frameNum = frameNums[clb]
    currentFrame = 0
    currentGif = gifs[clb]
    currentCallback = sequence[clb]
    mode = currentCallback['name']
    variables[mode] = callbacks[mode].variables(cam)
    root.title(f"live{currentCallback['name'][0].upper()}{currentCallback['name'][1:]}")

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

    img1 = ImageTk.PhotoImage(Image.new("RGB", (200, 200)))

    label = tkinter.Label(root, image = img1, borderwidth=0, highlightthickness=0)
    label.pack()

    root.bind("<Right>", nextCallback)
    root.bind("<Left>", prevCallback)
    root.bind("<Return>", callback)
    root.mainloop()