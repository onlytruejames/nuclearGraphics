# NuclearGraphics

![funni logo](https://raw.githubusercontent.com/onlytruejames/nuclearGraphics/main/nuclearGraphics.png)

This is some live graphics software I made in tkinter. It started from trying to replicate the [Looking At Your Pager](https://www.youtube.com/watch?v=Z2IwAKmY774) visuals in Python, it went well so I made more, then a way to switch between them. I also ~~plageurized~~ imitated effects from [live Aphex Twin graphics](https://www.youtube.com/watch?v=961uG4Ixg_Y) by [Weirdcore](http://weirdcore.tv), and I've [used it in a live performance before](https://www.instagram.com/p/CqgMcw5ohTc/). So here the code is for people to use if they are ~~deranged that they'd try and use this~~ so inclined.

## Premise

Essentially it takes a webcam image, then turns it from OpenCV to Pillow, combines it with a GIF if you want, passes it through a filter, then puts it on a Tkinter window.

## More detailed flow of the program

It figures out what webcam you want. If it finds multiple, it should ask you but idrk tbh. If it finds none, you've not plugged one in or not started a virtual one. If you already have, the port number is higher than 0, so fix it or *cope*.

Then it creates a webcam object. This is called fakeCam. This deals with merging GIFs with a photo from your webcam.

blah blah blah empty variable list because this updates every time you change effects, it's pointless to do it here too...

The GIFs are loaded, as well as the number of frames because contrary to popular belief, `Image.n_frames` barely works if at all, it never worked for me. Put the gifs in `/gifs` for them to be loaded. Number them, one for each effect you want. Also, count from 0, so the first effect loads `0.gif`, the second one does `1.gif`, etc. If you don't want a gif, omit `gifAmount` from the setlist for the effects you don't want it on.

Then a tkinter window is created and it has an image on it. To start, press enter. To switch effects, use the left and right arrows or click on the main bit of the window.

### On changing the effect

Gets the current gif, gets the required variables for the effect, changes the window title

### On each new frame

Calls `callback`, which gets the image from the effect, which gets it from `fakeCam`. It resizes it to fit the window, then puts it there.

I think that just about does it

## Programming in a sequence

1. Open `set.json`
2. There should be one effect in there already. The file will look like this:
```json
[
    {
        "name": "ascii",
        "gifAmount": 0.5
    }
]
```
3. Basically copy this over and over again in the list with different effects and Gif amounts, which are a value from 0 to 1 representing how much of the input video is from the Gif. The included effects are below, but you can use more if you add them
```json
"ascii"
"blurDart"
"circle"
"colourOffset"
"flipDiff"
"imgFX"
"kaleidoscope"
"maximum"
"mirrorEcho"
"oppDiff"
"pixSort"
"reciprocal"
"RGBSwapper"
"stretch"
```
4. If you want to add Gifs to the effect, put them in `gifs` and name them `0.gif`, `1.gif`, etc, for as many effects as you need. If an effect doesn't need a Gif, don't add a gif for the effect and you can also remove `gifAmount` from the sequence.
5. Done!

## Adding custom effects

1. Add the folder name to the imports at the very top of `main.py`
2. In `callbacks` in `main.py`, add `"[effect name]": [folder name]`
4. Done!

## Creating your own effect

1. Create a folder called `live[effect name]`
2. Add `__init__.py`
3. In `__init__.py`, add the following code:
```python
from PIL import (
    Image,
    ImageFilter
)

#constant variables here

def variables(cam):
    return [] #fill this list with the variables you need, although frankly it can be any data type as long as it's only one variable

def callback(cam, variables):
    #get your variables here with variables[0] or whatever
    result, image = cam.read()
    if result:
        #image is a PIL image which you can manipulate. Once manipulated, return the image.

```

4. Add the effect as outlined in the previous section.
5. Done!