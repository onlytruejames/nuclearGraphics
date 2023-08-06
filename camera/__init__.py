from cv2 import VideoCapture, cvtColor, COLOR_BGR2RGB
from PIL import Image

def variables(idg, af):
    return []

#stolen from stackoverflow
nonWorkingPorts = []
devPort = 0
ports = []
while not len(nonWorkingPorts):
    camera = VideoCapture(devPort)
    if camera.isOpened():
        isReading, img = camera.read()
        if isReading:
            ports.append(devPort)
        else:
            nonWorkingPorts.append(devPort)
    else:
        nonWorkingPorts.append(devPort)
    devPort +=1

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

cam = VideoCapture(port)

def callback(image, variables):
    result, img = cam.read()
    if not result:
        return image
    img = Image.fromarray(cvtColor(img, COLOR_BGR2RGB)).resize(image.size)
    return img