from PIL import Image
import random

def variables(dims, clb):
    global lastImg, level
    lastImg = Image.new("RGB", dims)
    level = 0
    return []

def callback(img, variables):
    global lastImg, level
    img = img.convert("RGBA")
    lastImg.putalpha(Image.new("L", lastImg.size, 127 + abs(level)))
    newLastImg = Image.new("RGBA", img.size)
    newLastImg.paste(lastImg, (
        int((img.width - lastImg.width) / 2),
        int((img.height - lastImg.height) / 2)
    ))
    img = Image.alpha_composite(img, newLastImg)
    lastImg = img.resize((img.width + level, img.height + level))
    level += random.randint(-25, 25)
    if level > 50:
        level = 50
    if level < -50:
        level = -50
    if -10 < level < 10:
        level *= 2
    if random.randint(0, 1000) == 420:
        level = random.randint(-50, 50)
    return img