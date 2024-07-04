from PIL import Image

global imgs
imgs = {}

def resizeImage(img1, img2, mode=0):
    #mode 0: don't cut off bits of img1
    #mode 1: don't leave any empty space
    sideRatio1 = img1.width / img1.height
    sideRatio2 = img2.width / img2.height
    #sideRadio = widthness
    if mode == 0:
        backdrop = Image.new("RGBA", img2.size)
        img1 = img1.convert("RGBA")
        if sideRatio1 > sideRatio2:
            #resize so widths are equal
            multiplier = img2.width / img1.width
            img1 = img1.resize((img2.width, int(img2.height * multiplier)))
            backdrop.paste(img1, (0, int((img2.height - img1.height) / 2)))
        else:
            #resize img1 so heights are equal
            multiplier = img2.height / img1.height
            img1 = img1.resize((int(img1.width * multiplier), img2.height))
            backdrop.paste(img1, (int((img2.width - img1.width) / 2), 0))
        return backdrop
    if mode == 1:
        if sideRatio1 > sideRatio2:
            #resize img1 so heights are equal
            multiplier = img2.height / img1.height
            img1 = img1.resize((int(img1.width * multiplier), img2.height))
            widDiff = int(img2.width - img1.width / 2)
            img1 = img1.crop((widDiff, 0, img2.width + widDiff, img2.height))
        else:
            #resize img1 so widths are equal
            multiplier = img2.width / img1.width
            img1 = img1.resize((img2.width, int(img2.height * multiplier)))
            hiDiff = int(img2.height - img1.height / 2)
            img1 = img1.crop((0, hiDiff, img2.width, img2.height + hiDiff))
    return img1

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
        return Image.alpha_composite(image, resizeImage(img, image).convert("RGBA"))
    except Exception as e:
        return image