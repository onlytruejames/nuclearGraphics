# NuclearGraphics

![funni logo](https://raw.githubusercontent.com/onlytruejames/nuclearGraphics/main/nuclearGraphics.png)

This is some live graphics software I made in tkinter. It started from trying to replicate the [Looking At Your Pager](https://www.youtube.com/watch?v=Z2IwAKmY774) visuals in Python, it went well so I made more, then a way to switch between them. I also ~~plageurized~~ imitated effects from [live Aphex Twin graphics](https://www.youtube.com/watch?v=961uG4Ixg_Y) by [Weirdcore](http://weirdcore.tv), and I've [used it in a live performance before](https://www.instagram.com/p/CqgMcw5ohTc/). So here the code is for people to use if they are ~~deranged that they'd try and use this~~ so inclined.

## what does this thing do

A blank image is passed through a bunch of filters/generators. The generators are `camera` and `loadImg` which just return a new image. The rest are effects. You can control how much an effect/generator affects the result, basically setting the alpha channel of the output to whatever. At the end it's all thrown in a tkinter window.

### On each new frame

For each effect, `callback` is called with the previous outputs.

### On window resizing

For each effect, the program attempts to call `changeDims` which can be used to recalculate/regenerate data which is meant to carry over across frames.

I think that just about does it

## Programming in a sequence

1. Create `set.json`
2. This is the format you follow. You can have as many effects as your cpu will tolerate before staging a revolution in which it overthrows you as its ruler and combusts:
```json
{
    "midi": true,
    "sequence": [
        [
            {
                "name": "effect 1",
                "amount": 1
            }, {
                "name": "effect 2",
                "amount": 1
            }, {
                "name": "effect 3",
                "amount": 1
            }
        ]
    ]
}
```
`name` determines what effect is used. `amount` is a float which determines how much of the effect you want. To convert to a RGBA Alpha value, multiply by 255.
3. Copy this over and over again in the list with different effects. The included effects are below, but you can use more if you add them. Effects can also be stacked and are executed in the order they appear in the `names` list.

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
"kuwahara"
"palette"
"dogBlur"
"zoom"
"saturate"
"dogShift"
"camera"
"loadImg"
"diffThresh"
"pixelate"
"change"
"colourRemover"
"brightThresh"
"sine"
"feedback"
"colourWheel"
"backgroundRemoval"
```
5. Done!

Also some of the effects have their own `set.json`s, but the documentation should be there instead (when I get round to it).

## Adding custom effects

1. Add the effect as a folder into the `effects` directory
2. List the folder name in `set.json`
3. Done!

## Creating your own effect

1. Create a folder named the effect name. 
2. Add `__init__.py`.
3. In `__init__.py`, add the following code:
```python
from PIL import Image

def variables(dims, clb):
    #called every time the effects are changed

def changeDims(dims):
    #only neccesary if you need to resize any variables

def callback(img):
    #do whatever to img which is a PIL image

```
`changeDims` is optional, I think `variables` is but I can't remember.
4. Done!