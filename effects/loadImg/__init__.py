from PIL import Image

global imgs
imgs = {}

def variables(dims, calb):
    global i, clb
    clb = str(calb)
    i = 0

def callback(image, variables):
    global clb, i, imgs
    if not variables["src"] in imgs:
        imgs[variables["src"]] = Image.open(f'effects/loadImg/{variables["src"]}')
    img = imgs[variables["src"]]
    try:
        try:
            img.seek(i)
        except:
            img.seek(0)
            i = -1
        i += 1
        return Image.alpha_composite(image, img.resize(image.size).convert("RGBA"))
    except Exception as e:
        return image