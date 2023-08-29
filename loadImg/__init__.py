from PIL import Image
import json

global imgs
imgs = json.load(open("loadImg/imgs.json", "r"))
newImgs = {}
for im in imgs:
    im = list(im.items())[0]
    newImgs[im[0]] = Image.open(f'loadImg/{im[1]}')
imgs = newImgs

def variables(dims, calb):
    global i, clb
    clb = str(calb)
    i = 0

def callback(image):
    global clb, i, imgs
    try:
        img = imgs[clb]
        try:
            img.seek(i)
        except:
            img.seek(0)
            i = -1
        i += 1
        return Image.alpha_composite(image, img.resize(image.size).convert("RGBA"))
    except Exception as e:
        return image