import json, tkinter, liveAscii, liveBlurDart, liveRGBSwapper, liveMirrorEcho, liveColourOffset
from PIL import Image, ImageTk, ImageFont
from cv2 import VideoCapture

callbacks = {
    "ascii": liveAscii,
    "blurDart": liveBlurDart,
    "RGBSwapper": liveRGBSwapper,
    "mirrorEcho": liveMirrorEcho,
    "colourOffset": liveColourOffset
}

global currentCallback, clb
clb = -1

sequence = json.load(open("set.json", "r"))

ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

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
    nextCallback(e)
    while True:
        img = callbacks[currentCallback].callback(cam, variables[currentCallback])
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

def changeCallback():
    global currentCallback, clb, root
    currentCallback = sequence[clb]
    root.title(f"live{currentCallback[0].upper()}{currentCallback[1:]}")

def nextCallback(e):
    global clb
    clb += 1
    changeCallback()

def prevCallback(e):
    global clb
    clb -= 1
    changeCallback()

if type(port) == int:
    global cam, root
    cam = VideoCapture(0)
    width = cam.get(3)
    height = cam.get(4)

    variables = {}

    for cb in callbacks.keys():
        variables[cb] = callbacks[cb].variables(cam)

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