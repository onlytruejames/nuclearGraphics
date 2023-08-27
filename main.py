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
import ascii, blurDart, rgbSwapper, mirrorEcho, colourOffset, imgFX, flipDiff, kaleidoscope, reciprocal, circle, maximum, oppDiff, pixSort, stretch, faceOnly, dissolve, kuwahara, palette, dogBlur, zoom, colourExpander, dogShift, camera, loadImg, diffThresh, pixelate, change, colourRemover, brightThresh, sine, feedback
from PIL import Image, ImageTk
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
    "camera": camera,
    "loadImg": loadImg,
    "diffThresh": diffThresh,
    "pixelate": pixelate,
    "change": change,
    "colourRemover": colourRemover,
    "brightThresh": brightThresh,
    "sine": sine,
    "feedback": feedback
}

global currentCallback, clb
clb = -1

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

def callback(e):
    global dims, transparent
    root.bind("<Button-1>", nextCallback)
    nextCallback(e)
    while True:
        msg = midiIn.poll()
        if msg:
            if msg.type == "note_on":
                nextCallback(e)
        try:
            newDims = (int(root.winfo_reqwidth() / 2), int(root.winfo_reqheight() / 2))
            if not dims == newDims:
                dims = newDims
                transparent = Image.new("RGBA", newDims, (0, 0, 0, 0))
                for cb in currentCallback:
                    try:
                        callbacks[cb["name"]].changeDims(newDims)
                    except:
                        continue
            image = Image.new("RGBA", dims)
            for cb in currentCallback:
                newImage = callbacks[cb["name"]].callback(image.convert("RGB")).convert("RGBA")
                newImage = Image.blend(transparent, newImage, cb["amount"])
                image = Image.alpha_composite(image, newImage)
            winWidth = root.winfo_width()
            winHeight = root.winfo_height()
            if winWidth / dims[0] > winHeight / dims[1]:
                resize = winHeight / dims[1]
            else:
                resize = winWidth / dims[0]
            img = image.resize((
                int(dims[0] * resize),
                int(dims[1] * resize)
            ))
            img = ImageTk.PhotoImage(img)
            label.configure(image = img)
            label.image = img
            root.update()
        except Exception as e:
            root.quit()
            raise e

def changeCallback():
    global currentCallback, clb, root, dims
    currentCallback = sequence[clb]
    #modes = currentCallback['names']
    #for mode in modes:
    #    variables[mode] = callbacks[mode].variables(cam, clb)
    for cb in currentCallback:
        try:
            callbacks[cb["name"]].variables(dims, clb)
        except:
            continue
        try:
            callbacks[cb["name"]].changeDims(dims)
        except:
            continue
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

global dims, transparent

root = tkinter.Tk()
dims = (root.winfo_reqwidth(), root.winfo_reqheight())
transparent = Image.new("RGBA", dims, (0, 0, 0, 0))

root.title("NuclearGraphics")

img1 = ImageTk.PhotoImage(Image.open("nuclearGraphics.png"))

label = tkinter.Label(root, image = img1, borderwidth=0, highlightthickness=0)
label.pack()

root.bind("<Right>", nextCallback)
root.bind("<Left>", prevCallback)
root.bind("<Return>", callback)
root.mainloop()