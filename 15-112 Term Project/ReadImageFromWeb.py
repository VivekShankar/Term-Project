from Tkinter import *
import ReadImageFromFile
def redrawAll(canvas):
    # Draw a double-size image on the right
    image = canvas.data["doubleImage2"]
    #imageSize = ( (image.width(), image.height()) )
    #msg = "Double-size " + str(imageSize)
    #ReadImageFromFile.run(canvas)
    canvas.create_image(canvas.width/2, 100, anchor=N, image=image)

import urllib
import os

def loadImageFromWeb(url):
    #assert(url.endswith(".gif")) # only works for gif's!
    try:
        fin = urllib.urlopen(url)
        imageData = fin.read()
    finally:
        fin.close()
    # save to tempfile and make image from that tempfile
    # (for now, just a relative file that we delete...)
    name = "_temp_image_.gif"
    try:
        tmp = open(name,"w+b")
        tmp.write(imageData)
    finally:
        tmp.close()
    try:
        image = PhotoImage(file=name)
    finally:
        os.remove(name)    
    # done!
    return image
   
def init(canvas, url):
    canvas.width = canvas.winfo_reqwidth()-4
    canvas.height = canvas.winfo_reqheight()-4
    #url = "http://kosbie.net/cmu/summer-08/15-100/handouts/pix/flagOfBosniaAndHerzegovina.gif"
    #url = "http://maps.google.com/maps/api/staticmap?maptype=roadmap&format=gif&size=200x200&sensor=false&markers=|label:H|4777%20Northfield%20Pkwy%2C%20Troy%2C%20MI%2048098&markers=|label:G|1359%20Torpey%20Dr%2C%20Troy%2C%20MI%2048083&markers=|label:A|163%20Cherry%20Dr.%2C%20Troy%2C%20MI"
    image = loadImageFromWeb(url)
    doubleImage = image.zoom(2,2)
    canvas.data["doubleImage2"] = doubleImage
    redrawAll(canvas)

########### copy-paste below here ###########

def run(canvas, url):
    #create the root and the canvas
    #Store canvas in root and in canvas itself for callbacks
    #Set up canvas data and call init
    #canvas.data = { }
    init(canvas, url)
    # set up events
    # root.bind("<Button-1>", leftMousePressed)
    # root.bind("<KeyPress>", keyPressed)
    # timerFired(canvas)
    # and launch the app
    #root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)
