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
    return []

def callback(image, variables):
    global clb, i, imgs
    try:
        img = imgs[clb]
        try:
            img.seek(i)
        except:
            img.seek(0)
            i = -1
        i += 1
        return img.resize(image.size)
    except Exception as e:
        print(e)
        return image