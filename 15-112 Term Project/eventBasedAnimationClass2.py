# eventBasedAnimationClass.py

from Tkinter import *
import sys

class EventBasedAnimationClass(object):
    def onMousePressed(self, event): pass
    def onTimerFired(self): pass
    def redrawAll(self): pass
    def initAnimation(self): pass

    def __init__(self, width=300, height=300):
        self.width = width
        self.height = height
        self.timerDelay = 100 # in milliseconds (set to None to turn off timer)

    def onMousePressedWrapper(self, event):
        if (not self._isRunning): return
        self.onMousePressed(event)
        self.redrawAll()

    def onTimerFiredWrapper(self):
        if (not self._isRunning): self.root.destroy(); return
        if (self.timerDelay == None): return # turns off timer
        self.onTimerFired()
        self.redrawAll()
        self.canvas.after(self.timerDelay, self.onTimerFiredWrapper)         

    def quit(self):
        if (not self._isRunning): return
        self._isRunning = False
        if (self.runningInIDLE):
            # in IDLE, must be sure to destroy here and now
            self.root.destroy()
        else:
            # not IDLE, then we'll destroy in the canvas.after handler
            self.root.quit()

    def run(self):
        # create the root and the canvas
        self.root = Tk()
        w=self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()
        #photo=PhotoImage(file='CloudBackground2.gif')
        #self.canvas.create_image(0, 0, image=photo, anchor=NW)
##        hbar=Scrollbar(self.root,orient=VERTICAL)
##        hbar.pack(side=RIGHT,fill=Y)
##        hbar.config(command=w.yview)
##        w.config(yscrollcommand=hbar.set)
        self.initAnimation()
        # set up events
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.quit())
        self._isRunning = True
        self.runningInIDLE =  ("idlelib" in sys.modules)
        # DK: You can use a local function with a closure
        # to store the canvas binding, like this:
        def f(event): self.onMousePressedWrapper(event)    
        self.root.bind("<Button-1>", f)
        # DK: Or you can just use an anonymous lamdba function, like this:
        self.onTimerFiredWrapper()
        # and launch the app (This call BLOCKS, so your program waits
        # until you close the window!)
        self.root.mainloop()

#EventBasedAnimationClass(300,300).run()
