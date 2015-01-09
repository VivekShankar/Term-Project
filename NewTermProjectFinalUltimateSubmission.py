#Name: Vivek Shankar, Andrew ID: vshanka1, Section: C                       ##
#Term Project:                                                              ##
#Application of Traveling Salesman Problem to Finding Optimal Round-Trip to ##
#A Series Of Locations                                                      ##
##############################################################################

##############################################################################
########################## Import Modules ####################################
##############################################################################

from Tkinter import *
from eventBasedAnimationClass2 import EventBasedAnimationClass
from googlemaps import GoogleMaps
from HTMLParser import HTMLParser
import copy
import webbrowser
import os
from motionless import DecoratedMap
from motionless import AddressMarker
from motionless import LatLonMarker
import ReadImageFromWeb
import ReadImageFromWeb2
import ReadImageFromWeb3
import ReadImageFromFile
import ReadImageFromFileUSAMap
import urllib
import math
from googleplaces import GooglePlaces, types, lang
import pygeocoder
import base64
import random

##############################################################################

#from http://stackoverflow.com/questions/753052/
#answer submitted by stackoverflow user Eloff
class MLStripper(HTMLParser):
    #class that parses string of HTML, removes tags
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)
    
##############################################################################    
##################################### Main Program ###########################
##############################################################################
    
class TSPSolver(EventBasedAnimationClass):
    #TSP Solver class

    def __init__(self):
        #initializes TSP Solver class
        width = height = 600
        super(TSPSolver, self).__init__(width,height)

##############################################################################
################################### Model ####################################
##############################################################################
        
    def initAnimation(self):
        #initializes basic variables to keep track of
        self.title = ('''Pathfinder''')
        self.root.title(self.title)
        self.yMargin = self.xMargin = 5
        self.citiesList = []
        self.computeDistances = False
        self.city = ''
        self.url = None
        self.distancesDict = {}
        self.initAnimationReadyState()
        self.error, self.order, self.gasStationError = None, None, None
        self.directionsText = ''
        self.initAnimationPageStates()
        self.isThereError = False
        self.isThereGasStationError = False
        self.initAnimationWidgetStates()
        self.actualMarkerCoords = None
        self.r = 5
        self.initAnimation2()
        self.initAnimationSplashScreen()

    def initAnimation2(self):
        #initializes basic variables to keep track of
        self.startingLoc = None
        self.orderToVisitDemo = None
        self.addresstext = StringVar()
        self.addAddressButton = None
        self.initAnimationButton1()
        self.initAnimationButton2()
        self.initAnimationButton3()
        self.initAnimationButton4()
        self.initAnimationButton5()
        self.initAnimationButton6()
        self.addressSelected = StringVar(self.root)
        self.radius = None
        self.readyToDrawAttractionsMap = False
        self.mapCityToLatLong = None
        self.deletedList = []
        self.initAnimationUndoRedoToggleCoords()
        self.showWeights = False
        self.demoTimerStep = 0
        self.startVar = IntVar()

    def initAnimationSplashScreen(self):
        #initializes variables pertaining to splash screen
        self.totalOpt2Distance = None
        self.greedyChoice = True
        self.pointList = self.createRandomPoints()
        self.greedyPointList = self.findClosestPoint(self.pointList)
        self.totalDistance = self.findTotalTwoOptAlgDist(self.greedyPointList)
        self.twoOptPointList = self.twoOptAlg(self.greedyPointList)
        self.timerStep = 0

    def initAnimationReadyState(self):
        #initializes variables to represent when it is "ready"
        #to move on to next stages of projects
        self.readyToDoGreedyAlg = False
        self.readyToDrawLines = False
        self.readyToPutStaticMap = False
        self.readyToSolve = False
        self.readyToDrawOrder = False

    def initAnimationWidgetStates(self):
        #initializes widget variables
        self.dropDownMenu = None
        self.dropDownRadiusMenu = None
        self.goButton = None
        self.getInfoButton = None
        self.infobox = None
        self.rentry = None
        self.listbox = None
        self.addressInputBox = None
        self.orderedAddressesBox = None
        self.entry = None
        self.finalDest = None

    def initAnimationPageStates(self):
        #initializes variables to keep track of what page user is on
        self.showAddressesPage = False
        self.showDirectionsText = False
        self.showDemosPage = False
        self.showAttractionsPage = False
        self.showInstructionsPage = False
        self.showSplashScreen = True

    def initAnimationUndoRedoToggleCoords(self):
        #initializes variables for coordinates of corners of undo, redo, &
        #toggle buttons
        self.x0 = 30
        self.y0 = 130
        self.x1 = 70
        self.y1 = 150
        self.togglex0 = self.width/2
        self.toggley0 = 550
        toggleButtonWidth = 100
        toggleButtonHeight = 20
        self.togglex1 = self.togglex0 + toggleButtonWidth
        self.toggley1 = self.toggley0 + toggleButtonHeight
        (self.startx0, self.starty0, self.startx1, self.starty1) = (400,500,
                                                                    500,540)

    def initAnimationButton1(self):
        #initializes button - address order
        self.buttonFrame = Frame(self.root)
        def b1Pressed():
            self.buttonGetAddresses()
            self.createInputAddressBox()
            self.createOrderedAddressBox()
        b1 = Button(self.buttonFrame, text="Address Order",command=b1Pressed)
        b1.grid(row=0,column=0)

    def initAnimationButton2(self):
        #initializes button - Directions
        numCities = 2 #once there are 2 cities inputted
        def b2Pressed():
            if (len(self.citiesList) >= numCities and self.order != None
                and len(self.order) >= numCities):
                self.buttonGetDirections()
        b2 = Button(self.buttonFrame, text = "Directions", command=b2Pressed)
        row = 0
        col = 1
        b2.grid(row=row,column=col)

    def initAnimationButton3(self):
        #initializes button - Map
        numCities = 2 #once there are 2 cities inputted
        def b3Pressed():
            if (len(self.citiesList) >= numCities and self.order != None
                and len(self.order) >= numCities):
                self.buttonGetMap()
        b3 = Button(self.buttonFrame, text = "Map",command=b3Pressed)
        row = 0
        col = 2
        b3.grid(row=row,column=col)

    def initAnimationButton4(self):
        #initializes button - TSP Algorithm Demo
        numCities = 2 #once there are 2 cities inputted
        def b4Pressed():
            if (len(self.citiesList) >= numCities and
                self.order != None and len(self.order) >= numCities):
                self.buttonDemos()
        b4 = Button(self.buttonFrame,text ="TSP Algorithm Demo",
                    command=b4Pressed)
        row = 0
        col = 3
        b4.grid(row=row,column=col)

    def initAnimationButton5(self):
        #initializes button - Gas Stations
        numCities = 2 #once there are 2 cities inputted
        def b5Pressed():
            if (len(self.citiesList) >= numCities and self.order != None
                and len(self.order) >= numCities):
                self.buttonAttractions()
        b5 = Button(self.buttonFrame,text ="Gas Stations",command=b5Pressed)
        row = 0
        col = 4
        b5.grid(row=row,column=col)

    def initAnimationButton6(self):
        #initializes button - Instructions
        def b6Pressed():
            self.buttonInstructions()
        b6 = Button(self.buttonFrame, text = "Help", command=b6Pressed)
        row = 0
        col = 5
        b6.grid(row=row,column=col)
        self.buttonFrame.pack(side=BOTTOM)

    def addressAdder(self):
        #adds addresses to list of cities in response to "Add Address" button
        self.isThereError = False
        city = ''.join(self.addresstext.get())
        numCities = 8
        if len(self.citiesList) <= numCities:
            if city != '' and city not in self.citiesList:
                try:
                    self.distancesDict = self.getDistances(city,
                                                       self.citiesList,
                                                       self.distancesDict)
                    if len(self.citiesList) == 0:
                        gmaps = GoogleMaps()
                        dirs=gmaps.directions(city,'163 Cherry Dr., Troy, MI')
                    self.citiesList += [city]
                    self.deletedList = []
                except Exception as err:
                    self.isThereError = True
                    self.error = "Unknown Address"
                    
##############################################################################        
################################ View ########################################
##############################################################################
                    
    def createEntryBox(self):
        #creates entry box widget for entering addresses
        xLength = 25
        self.entry = Entry(self.root,textvariable=self.addresstext,width=
                           xLength)
        xLoc, yLoc = 210, 540
        self.entry.place(x=xLoc,y=yLoc)

    def createFinalDestCheckBox(self):
        #creates final destination check box widget
        self.finalDest = Checkbutton(self.root, text='Go to Start?',
                                     variable = self.startVar,
                                     onvalue = 1, offvalue = 0)
        xLoc, yLoc = 435, 575
        self.finalDest.place(x=xLoc,y=yLoc)

    def createInputAddressBox(self, xLoc=20,yLoc=20):
        #creates input addresses box
        if self.addressInputBox != None:
            self.addressInputBox.destroy()
            self.addressInputBox = None
        #if widget were already there, destroy it and create a new one
        if len(self.citiesList) >= 1:
            listBoxWidth, listBoxHeight = 30, 4
            self.addressInputBox = Listbox(self.root, width=listBoxWidth,
                                           height=listBoxHeight)
            self.addressInputBox.place(x=xLoc,y=yLoc)
            count = 1
            for city in self.citiesList:
                self.addressInputBox.insert(END, str(count) + '. ' +
                                            city)
                count += 1

    def createOrderedAddressBox(self):
        #creates ordered addresses box
        if self.orderedAddressesBox != None:
            self.orderedAddressesBox.destroy()
            self.orderedAddressesBox = None
        #if widget were already there, destroy it and create a new one
        if self.order != None and len(self.order) >= 1:
            listBoxWidth, listBoxHeight = 30, 4
            self.orderedAddressesBox = Listbox(self.root, width=listBoxWidth,
                                               height=listBoxHeight)
            xLoc, yLoc = 340, 20
            self.orderedAddressesBox.place(x=xLoc,y=yLoc)
            count = 1
            for city in self.order:
                self.orderedAddressesBox.insert(END, str(count) + '. ' +
                                            city)
                count += 1

    def drawLabels(self):
        #draws labels onto canvas
        self.drawErrorLabel()

    def drawErrorLabel(self):
        #draws error label onto canvas if there is an error
        yLoc = 590
        if self.isThereError == True:
            self.canvas.create_text(self.width/2, yLoc,
                                    text = self.error, anchor = CENTER)
            
    def drawGasStationErrorLabel(self):
        #draws gas station error label onto canvas if there is an error
        yLoc = 590
        xLoc = 340
        yMargin = 10
        xMargin = 3
        if self.isThereGasStationError == True:
            self.canvas.create_rectangle(xLoc-xMargin,yLoc-yMargin
                                         , self.width,self.height,
                                         fill = 'cyan')
            self.canvas.create_text(xLoc, yLoc,
                                    text = self.gasStationError,
                                    anchor = W)

    def drawShowWeightsLabel(self):
        #draws relative weights of edges in TSP Algorithm demo
        x0 = self.togglex0
        y0 = self.toggley0
        x1 = self.togglex1
        y1 = self.toggley1
        margin = 2
        self.canvas.create_rectangle(x0,y0,x1,y1,fill='yellow')
        self.canvas.create_text(x0+margin,y0+margin,
                                text='Toggle Weights',anchor=NW)

    def createUndoRedoLabels(self):
        #draws undo redo "button" labels onto canvas
        x0 = self.x0
        y0 = self.y0
        x1 = self.x1
        y1 = self.y1
        xMid = (x0+x1)/2
        yMid = (y0+y1)/2
        deltaY = 30
        redoChangeHeight = 30
        self.canvas.create_rectangle(x0,y0,x1,y1,fill = 'yellow')
        self.canvas.create_text(xMid,yMid,text='Undo',anchor=CENTER)
        self.canvas.create_rectangle(x0,y0+deltaY,x1,y1+deltaY,fill = 'yellow')
        self.canvas.create_text(xMid,yMid+deltaY,text='Redo',anchor=CENTER)

    def drawDirectionsText(self):
        #draws directions text onto canvas
        xMargin = yMargin = 5
        self.canvas.create_text(self.width/2, yMargin,
                                text='Directions for Trip', anchor = N)
        self.canvas.create_text(xMargin,yMargin,text=self.directionsText,
                                anchor = NW)

    def drawPointsOnMarkers(self):
        #draws blue ovals onto markers (TSP Algorithm Demo)
        r = self.r
        if self.actualMarkerCoords != None:
            for coord in self.actualMarkerCoords:
                self.canvas.create_oval(coord[0]-r,coord[1]-r,
                                        coord[0]+r,coord[1]+r, fill = 'black',
                                        outline = 'orange')
        self.readyToDrawLines = True

    def drawLinesBetweenPoints(self):
        #draws lines between every pair of markers (TSP Algorithm Demo)
        if self.readyToDrawLines == True:
            for coord1 in self.actualMarkerCoords:
                for coord2 in self.actualMarkerCoords[1:]:
                    self.canvas.create_line(coord1,coord2)

    def drawWeightsOnLines(self):
        #draws numbers on edges to represent the relative distances between
        #markers
        if self.readyToDrawLines == True and self.showWeights == True:
            for coord1 in self.actualMarkerCoords:
                for coord2 in self.actualMarkerCoords[1:]:
                    dist = round(math.sqrt((coord1[0] - coord2[0])**2 +
                                           (coord1[1] - coord2[1])**2),1)
                    #distance formula
                    midPointX = (coord1[0]+coord2[0])/2.0
                    midPointY = (coord1[1]+coord2[1])/2.0
                    #midpoint formula
                    if dist != 0.0:
                        self.canvas.create_text(midPointX, midPointY,
                                                text=str(dist), anchor=NW)

    def drawOrderToVisitDemo(self):
        #draws blue line representing optimal path generated by TSP
        #Greedy Algorithm (simulation)
        start = self.timerStep
        if self.startingLoc != None:
            thickness = 5 #width of path
            numLines = self.demoTimerStep/2
            numLines = numLines % (len(self.orderToVisitDemo)+1)
            for index in xrange(numLines):
                if index == (len(self.orderToVisitDemo) - 1):
                    self.canvas.create_line(self.orderToVisitDemo[-1],
                                            self.orderToVisitDemo[0],
                                            fill = 'blue',
                                            width=thickness)
                else:
                    self.canvas.create_line(self.orderToVisitDemo[index],
                                            self.orderToVisitDemo[index+1],
                                            fill = 'blue',
                                            width=thickness)

    def redrawAllAddressesPage(self):
        #redraw all for addresses page
        if self.showAddressesPage == True:
            self.canvas.delete(ALL)
            fontType = 'MaturaMTScriptCapitals 14'
            ReadImageFromFile.run(self.canvas)
            margin, thick = 200, 10
            x0, y0, x1, y1 = (self.width/2 - margin, self.height/2 - margin,
                              self.width/2 + margin, self.height/2 + margin)
            self.canvas.create_rectangle(x0,y0,x1,y1,outline='red',width=thick)
            #border for map
            textxLoc, textyLoc, orderxLoc, orderyLoc = 100, 10, 420, 10
            self.canvas.create_text(textxLoc,textyLoc,text="Addresses",
                                    fill='black',font=fontType,anchor = W)
            self.canvas.create_text(orderxLoc,orderyLoc, font = fontType,
                                    text="Order to Visit",fill='black',anchor=W)
            errorx0, errory0, errorx1, errory1 = 170, 580, 430, 600
            self.canvas.create_rectangle(errorx0,errory0,errorx1,
                                         errory1, fill = 'cyan2')
            self.createUndoRedoLabels()
            self.drawLabels()
            self.makeStaticImage()

    def redrawAllDemosPage(self):
        #redraw all for demos page
        if self.showDemosPage == True:
            self.canvas.delete(ALL)
            fontType = 'MaturaMTScriptCapitals 14'
            ReadImageFromFile.run(self.canvas)
            self.canvas.create_text(self.width/2,self.yMargin,
                                    text="TSP Algorithm Demos",
                                    font = fontType,
                                    anchor=N)
            self.makeStaticImage()
            x0, y0, x1, y1 = 90, 90, 510, 510
            xLength = 10
            self.canvas.create_rectangle(x0,y0,x1,y1,outline= 'red',
                                         width =xLength)
            self.drawPointsOnMarkers()
            self.drawLinesBetweenPoints()
            self.drawWeightsOnLines()
            if self.orderToVisitDemo != None:
                self.drawOrderToVisitDemo()
            self.drawShowWeightsLabel()

    def redrawAllDirectionsText(self):
        #redraw all for directions text page
        if self.showDirectionsText == True:
            self.canvas.delete(ALL)
            ReadImageFromFile.run(self.canvas)

    def redrawAllAttractionsPage(self):
        #redraw all for attractions page
        if self.showAttractionsPage == True:
            self.canvas.delete(ALL)
            ReadImageFromFile.run(self.canvas)
            if self.readyToDrawAttractionsMap == True:
                self.makeStaticImage2()
            x0, y0, x1, y1 = 440,240,580,290
            self.canvas.create_rectangle(x0,y0,x1,y1,fill = "light blue")
            textxLoc, textyLoc = 450, 250
            self.canvas.create_text(textxLoc, textyLoc,
                                    text="Enter Radius Below\n(miles)",
                                    anchor = NW)
            borderx0, bordery0, borderx1, bordery1 = 20, 20, 420, 420
            xLength = 10
            self.canvas.create_rectangle(borderx0,bordery0,borderx1,bordery1,
                                         outline= 'red', width =xLength)
            xLoc, yLoc = 470,450
            self.canvas.create_text(xLoc, yLoc,text='Addresses',
                                    font='MaturaMTScriptCapitals 14')
            self.drawGasStationErrorLabel()

    def drawTitlesSplashScreen(self):
        #draws titles onto splash screen
        title1 = '''Application of Traveling Salesman Problem'''
        title2 = '''Pathfinder'''
        yLoc1, yLoc2 = 30, 70
        self.canvas.create_text(self.width/2, yLoc1,
                                text=title1,
                                font = 'MaturaMTScriptCapitals 28',
                                fill = 'blue', anchor = CENTER)
        self.canvas.create_text(self.width/2, yLoc2, text = title2,
                                font = 'MaturaMTScriptCapitals 28',
                                fill = 'blue', anchor = CENTER)

    def redrawAllSplashScreen(self):
        #redraw all for splash screen
        if self.showSplashScreen == True:
            self.canvas.delete(ALL)
            if self.greedyChoice == True:
                pointList =self.greedyPointList
                #DON't Do this in redraw all
            elif self.greedyChoice == False:
                pointList = self.twoOptPointList
            mapURL = 'http://votefamilyvalues.com/us_map.gif'
            ReadImageFromFileUSAMap.run(self.canvas)
            self.drawTitlesSplashScreen()
            self.drawRandomPointsOnScreen()
            self.createStartButton()
            x0,y0,x1,y1=225,510,375,530
            self.canvas.create_rectangle(x0,y0,x1,y1, fill = 'cyan')
            #Total distance label
            numLines, numPoints = self.timerStep/2, 25
            numLines = numLines % (numPoints + 1)
            for i in xrange(numLines):
                self.createSimulation(numLines, numPoints, i, pointList)
            self.drawAlgorithmLabels()

    def createSimulation(self, numLines, numPoints, i, pointList):
        #draws lines for greedy and opt-2 algorithm simulations (splash screen)
        #draws total distance traveled at each step in simulation
        y0, xLength = 520, 3
        if self.greedyChoice == True and i == numLines-1:
            xLoc, yLoc = self.width/2,y0
            self.canvas.create_text(xLoc,yLoc,text= 'Total Distance: ' +
                                    str(self.totalDistance[i+1]))
        elif self.greedyChoice == False and i == numLines-1 and i>=0:
            xLoc, yLoc = self.width/2,y0
            self.canvas.create_text(xLoc,yLoc,text= 'Total Distance: ' +
                                    str(self.totalOpt2Distance[i+1]))
        if i == numPoints - 1:
            self.canvas.create_line(pointList[-1],pointList[0],
                                    fill = 'blue', width = xLength)
        else:
            self.canvas.create_line(pointList[i],pointList[i+1],
                                    fill = 'blue', width = xLength)
        
    def drawAlgorithmLabels(self):
        #draws algorithm labels onto splash screen
        xLoc, yLoc = 300, 550
        xMargin, yMargin = 75, 10
        ySwitch = 490
        self.canvas.create_rectangle(xLoc-xMargin,yLoc-yMargin
                                     ,xLoc+xMargin,yLoc+yMargin,
                                     fill='yellow')
        self.canvas.create_rectangle(xLoc-xMargin,ySwitch-yMargin
                                     ,xLoc+xMargin,ySwitch+yMargin,
                                     fill='yellow')
        if self.greedyChoice == True:
            self.canvas.create_text(xLoc,yLoc,text='Greedy Algorithm')
            self.canvas.create_text(self.width/2,ySwitch,
                                    text='Switch to 2-Opt')
        if self.greedyChoice == False:
            self.canvas.create_text(xLoc,yLoc,text='2-Opt Algorithm')
            self.canvas.create_text(self.width/2,ySwitch,
                                    text='Switch to Greedy')

    def createStartButton(self):
        #draws start button on splash screen
        x0,y0,x1,y1 = 400,500,500,540
        xMargin, yMargin = 50, 20
        self.canvas.create_rectangle(x0,y0,x1,y1,fill = 'cyan')
        self.canvas.create_text(x0+xMargin,y0+yMargin,text='Start',
                                font='MaturaMTScriptCapitals 28',
                                anchor = CENTER)

    def drawRandomPointsOnScreen(self):
        #draws random points onto map of USA on splash screen
        r = 3
        pointList = self.pointList
        for index in xrange(len(pointList)):
            x, y = pointList[index][0], pointList[index][1]
            if index == 0:
                self.canvas.create_oval(x-r,y-r,x+r,y+r, fill = 'red')
                #starting location is red
            else:
                self.canvas.create_oval(x-r,y-r,x+r,y+r, fill = 'black')

    def redrawAllInstructionsPage(self):
        #redraw all for instructions page
        if self.showInstructionsPage == True:
            self.canvas.delete(ALL)
            ReadImageFromFile.run(self.canvas)
            self.canvas.create_text(self.width/2,15,text='Instructions',
                                    font = 'MaturaMTScriptCapitals 28',
                                    fill = 'blue',
                                    anchor = CENTER)
            instructionsText = '''Click the "Start" button to get started.
Type in the address of your starting location in the text bar and press "Add Address."
Notice that your address has been added to the "Addresses" box.
Continue to add more addresses by repeating the previous step.
Then, press the "Address Order" button to determine the optimal order to visit
the input addresses according to the Greedy Algorithm.
The optimal order will be displayed in the "Order to Visit" box.
Click undo to delete previously entered addresses, and redo to enter them back.
If you want to return to your starting location, check the "Go to start?" check box.
Note that until you enter at least 2 cities, none of the remaining buttons will work.

Press the "Directions" button to get the step-by-step driving directions
in a text-based format for your trip.
Press the "Map" button to open a map in your browser with scroll/zoom features
depicting a visual representation of the route.

Press the "TSP Algorithm Demo" button to view a simulation of the TSP greedy algorithm
finding the optimal route through the entered addresses.
The simulation is overlaid on a map with nodes corresponding to actual locations entered.
A blue node corresponds to each marker location. The markers are numbered corresponding
to the order the addresses were entered in the "Addresses box."
Notice that if some entered markers are very close together/overlapping, the demo will
approximate them as one marker collectively.
Click a node to begin the simulation. The algorithm will treat the "clicked node" as the
starting location and find the optimal round-trip path according to the TSP Greedy Algorithm.
Click the "Toggle Weights" button to show the relative distances between any pair of nodes.

Press the "Gas Stations" button to find nearby gas stations to any location on your trip.
Pick an address and a radius from the "Addresses" and "Radius" drop down menus.
Then, press "Go!" to find all gas stations within the specified radius from
the address.
The address is shown as a red marker, and the gas stations are shown as blue markers.
Press the "Get Info" button to display a key showing the name and address of each gas station.
To add a gas station into the list of addresses you want to visit, simply double-click
the address of the gas station in the box to add it to the "Addresses" box.  
'''
            xLoc, yLoc = 5, 30
            self.canvas.create_text(xLoc,yLoc,text=instructionsText,anchor=NW)

    def redrawAll(self):
        #redraws everything onto canvas
        self.redrawAllAddressesPage()
        self.redrawAllDemosPage()
        self.redrawAllDirectionsText()
        self.redrawAllAttractionsPage()
        self.redrawAllSplashScreen()
        self.redrawAllInstructionsPage()

##############################################################################           
################################### Controller ###############################
##############################################################################
        
    def onTimerFired(self):
        #updates timer count related variables every timer fired
        self.timerStep += 1
        if self.startingLoc != None:
            self.demoTimerStep += 1

    def onMousePressed(self, event):
        #performs mouse-pressed related events
        if self.showSplashScreen == True:
            self.onMousePressedSplashScreen(event.x, event.y)
        if self.showAddressesPage == True:
            #undo and redo if user clicks on corresponding labels
            if self.withinUndoLabel(event.x, event.y): self.undo()
            elif self.withinRedoLabel(event.x, event.y): self.redo()
        if self.showDemosPage == True:
            if self.readyToDoReadyAlg == True:
                for coordPair in self.actualMarkerCoords:
                    if (self.contains(event.x,event.y,
                                      coordPair[0],coordPair[1])):
                        #start greedy algorithm if user clicks on a point
                        #use point user clicked on as starting location
                        self.demoTimerStep = 0
                        self.startingLoc = coordPair
                self.greedyAlgorithmDemo()
            if self.withinToggleWeightsLabel(event.x, event.y):
                #turn on/off weights if user clicks toggle weights label
                self.showWeights = not self.showWeights

    def onMousePressedSplashScreen(self, eventX, eventY):
        #performs mouse-press events on splash screen page
        if self.withinStartLabel(eventX, eventY):
            self.buttonGetAddresses()
        if self.withinToggleAlgLabel(eventX,eventY):
            self.greedyChoice = not self.greedyChoice
            #go to input addresses page if user clicks on start
        
    def createRandomPoints(self):
        #creates random points to be drawn onto map of USA (splash screen)
        numPoints = 25
        pointList = []
        margin = 10
        x0 = 50 
        x1 = 500
        y0 = 150
        y1 = 350 #approx bounds for USA map (so points are randomly
        #drawn on top of the USA map)
        for i in xrange(numPoints):
            x = random.randint(x0,x1)
            y = random.randint(y0,y1)
            pointList += [(x,y)]
        return pointList

    def findClosestPoint(self, pointList, totalDistance=[]):
        #recursively finds the optimal order in which to visit the randomly
        #chosen points on the splash screen according to Greedy Algorithm
        if len(pointList) == 1:
            self.totalDistance = totalDistance
            return pointList
        firstPoint = pointList[0]
        closestPoint, minDistance = None, None
        for point2 in pointList[1:]:
            dist = round(math.sqrt((firstPoint[0] - point2[0])**2 +
                                   (firstPoint[1]-point2[1])**2))
            if dist < minDistance or minDistance == None:
                closestPoint = point2
                minDistance = dist
        #finds next closest point
        if len(totalDistance) >= 1:
            totalDistance.append(minDistance+totalDistance[-1])
        else: totalDistance.append(minDistance)
        closestPointIndex = pointList.index(closestPoint)
        pointList = ([closestPoint] + pointList[1:closestPointIndex]
                     + pointList[closestPointIndex+1:])
        #removes previous point from pointList, make point we are on
        #the first element in the "revised" pointList
        return [firstPoint] + self.findClosestPoint(pointList, totalDistance)

    def dist(self, a,b):
        #a, b are tuples a = (x0,y0), b = (x1,y1)
        #returns Euclidean distance from point a to point b
        return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

    def twoOptAlg(self, pointList):
        #takes in a pointList, performs two-opt algorithm on the points,
        #returns the optimal route according to two-opt algorithm
        done = False
        while not done:
            noChange = True #tracks whether swap has been made
            for index1 in xrange(len(pointList)):
                edgePair1 = self.findEdgePair1(index1,pointList)
                for index2 in xrange(index1+2,len(pointList)):
                    edgePair2 = self.findEdgePair2(index2, pointList)
                    currentDist2 = self.findTotalTwoOptAlgDist(pointList)[-1]
                    currentDist = (self.dist(edgePair1[0],edgePair1[1]) +
                                   self.dist(edgePair2[0],edgePair2[1]))
                    newPointList = self.makeSwap(pointList,index1,index2)
                    #performs the swap
                    newDist2 = self.findTotalTwoOptAlgDist(newPointList)[-1]
                    newDist = (self.dist(edgePair1[0],edgePair2[0]) +
                               self.dist(edgePair1[1],edgePair2[1]))
                    #distance with swap
                    if newDist < currentDist: #make the swap
                        pointList, noChange = newPointList, False
                        break
                else: continue
                break #break out of nested for loops and find swaps again
            if noChange == True: done = True
        self.totalOpt2Distance = self.findTotalTwoOptAlgDist(pointList)
        return pointList

    def findEdgePair1(self, index1, pointList):
        #finds first edge in 2-opt algorithm
        if index1 == len(pointList)-1:
            edgePair1 = (pointList[index1],pointList[0])
        else: edgePair1 = (pointList[index1],pointList[index1+1])
        return edgePair1
        #include the edge between the first and last points

    def findEdgePair2(self, index2, pointList):
        #finds second edge in 2-opt algorithm
        #pick a 2nd edge (non-adjacent to the first)
        if index2 == len(pointList)-1:
            edgePair2 = (pointList[index2],pointList[0])
        else: edgePair2 = (pointList[index2],pointList[index2+1])
        return edgePair2
        #include the edge between the first and last points

    def makeSwap(self, pointList, index1, index2):
        #swaps 2 non-adjacent edges and returns revised pointList
        newPointList = (pointList[:index1+1]+[pointList[index2]]+
                        pointList[index1+2:index2]+
                        [pointList[index1+1]]+ pointList[index2+1:])
        return newPointList

    def findTotalTwoOptAlgDist(self, pointList):
        #finds total two-opt algorithm distance at each stage
        #returns the distances as a list
        totalDistance = [0]
        for i in xrange(len(pointList)):
            if i == len(pointList)-1:
                distance = round(self.dist(pointList[i],pointList[i-1]),1)
                totalDistance.append(distance+totalDistance[i-1])
                finalDistance = round(self.dist(pointList[i],pointList[0]),1)
                totalDistance.append(finalDistance+totalDistance[i])
            elif i >= 1:
                distance = round(self.dist(pointList[i],pointList[i-1]),1)
                totalDistance.append(distance+totalDistance[i-1])
        return totalDistance
                                  
    def contains(self, x0, y0, x, y):
        #return True if (x0,y0) (mouse click) is within circle
        #with radius r, centered around (x,y) else return False
        return ((x0 - x)**2 + (y0 - y)**2 <= self.r**2)

    def undo(self):
        #undos the previously input city (deletes city)
        if len(self.citiesList) >= 1:
            self.deletedList += [self.citiesList[-1]]
            pairsToDelete = []
            for pair in self.distancesDict:
                if (pair[0] == self.citiesList[-1] or
                    pair[1] == self.citiesList[-1]):
                    pairsToDelete += [pair]
            for pair in pairsToDelete:
                del self.distancesDict[pair]
            #delete all pairs corresponding to deleted address in distances
            #dictionary
            if self.order != None and self.citiesList[-1] in self.order:
                self.order.remove(self.citiesList[-1])
            #delete the city from the ordered addresses list as well
            self.citiesList = self.citiesList[:-1]
            #recreate the address boxes to clearly display result of undo 
            self.createInputAddressBox()
            self.createOrderedAddressBox()

    def redo(self):
        #redos previous cities if they have been "undone"
        if len(self.deletedList) >= 1:
            self.distancesDict = self.getDistances(self.deletedList[-1],
                                                   self.citiesList,
                                                   self.distancesDict)
            self.citiesList += [self.deletedList[-1]]
            self.deletedList = self.deletedList[:-1]
            #remove redone city from deleted list, add it to cities list,
            #distances dictionary
            self.createInputAddressBox()

    def withinToggleAlgLabel(self, x0, y0):
        #returns True if mousePressed (x0,y0) lies within the toggle
        #Algorithm label, False otherwise
        xLeft, xRight = 225, 375
        yDown, yTop = 480, 500
        return xLeft <= x0 <= xRight and yDown <= y0 <= yTop

    def withinUndoLabel(self, x0, y0):
        #returns True if mousePressed (x0, y0) lies within the undo label
        #False otherwise
        return self.x0 <= x0 <= self.x1 and self.y0 <= y0 <= self.y1

    def withinRedoLabel(self, x0, y0):
        #returns True if mousePressed (x0, y0) lies within the redo label,
        #False otherwise
        margin = 30
        return (self.x0 <= x0 <= self.x1 and
                self.y0+margin <= y0 <= self.y1+margin)

    def withinToggleWeightsLabel(self, x0, y0):
        #returns True if mousePressed (x0, y0) lies within the toggle weights
        #label, False otherwise
        return (self.togglex0 <= x0 <= self.togglex1 and
                self.toggley0 <= y0 <= self.toggley1)

    def withinStartLabel(self, x0, y0):
        #returns True if mousePressed (x0, y0) lies within the start
        #label on Splash Screen page, False otherwise
        return (self.startx0 <= x0 <= self.startx1 and
                self.starty0 <= y0 <= self.starty1)

    def getDistances(self, start, selectedList, distances):
        #returns dictionary of all distances between all locations currently
        #listed
        for address in selectedList:
            gmaps = GoogleMaps()
            dirs = gmaps.directions(start, address)
            distances[(address,start)]=dirs['Directions']['Distance']['meters']
        return distances

    def greedyAlgorithm(self, selectedList, distancesDict):
        #recursively applies TSP greedy algorithm to find optimal
        #order of addresses to visit (according to distance)
        if self.readyToSolve:
            if len(selectedList) == 1: return []
            minDistance, minPoint, cityPair = None, None, None
            for pair in distancesDict:
                if selectedList[0] in pair:
                    if (distancesDict[pair]<minDistance or minDistance==None):
                        minDistance, cityPair = distancesDict[pair], pair
                        if selectedList[0] != pair[0]:
                            minPoint = pair[0]
                        else: minPoint = pair[1]
            #find the closest point of the remaining points
            pairsToDelete = []
            for pair in distancesDict:
                if pair[0] == selectedList[0] or pair[1] == selectedList[0]:
                    pairsToDelete += [pair]
            #delete all keys with previous point (no going back in Greedy Alg)
            for pair in pairsToDelete: del distancesDict[pair]
            i = selectedList.index(minPoint)
            #the next point becomes the starting point
            selectedList = [minPoint] + selectedList[1:i] + selectedList[i+1:]
            return [minPoint]+self.greedyAlgorithm(selectedList, distancesDict)

    #from http://stackoverflow.com/questions/753052/
    #answer submitted by stackoverflow user Eloff
    @staticmethod
    def strip_tags(html):
        #takes in html string, strips html tags
        s = MLStripper()
        s.feed(html)
        return s.get_data()

    def getRoute(self, gmaps, start, end):
        #takes in gmaps instance of GoogleMaps class, start, end
        #returns directions, route, distance from start to end
        dirs = gmaps.directions(start, end)
        route = dirs['Directions']['Routes'][0]
        dist = dirs['Directions']['Distance']['meters']
        return dirs, route, dist

    def getDirectionsText(self):
        #creates text of directions to go to the addresses input by user
        #stores them in variable - self.directionsText
        gmaps, totalDistance = GoogleMaps(), 0
        for index in xrange(1,len(self.order)):
            start, end = self.order[index-1], self.order[index]
            dirs, route, dist = self.getRoute(gmaps, start, end)
            totalDistance += dist
            conv, conv2 = 1609.34, 5280 #num meters per mile, feet per mile
            dist = str(round((int(dist)/float(conv)), 1))
            self.directionsText += "\nDirections from %s to %s \n" % (start,end)
            self.directionsText += "Total Distance: %s miles \n\n" % (dist) 
            for step in route['Steps']:
                distance = str(round(step['Distance']['meters']/float(conv),
                                     1))+' miles'
                if distance == '0.0 miles':
                    distance = str(round(step['Distance']['meters']/float(conv)
                                         *conv2))+' feet'
                self.directionsText += (TSPSolver.strip_tags
                                        (step['descriptionHtml'])
                                        + '\n' + distance + '\n')
        self.getDirectionsToStartText(gmaps,totalDistance,conv,conv2)

    def getDirectionsToStartText(self,gmaps,totalDistance,conv,conv2):
        #adds text of directions to go back to the starting location
        if self.startVar.get() == 1:
            start, end = self.order[-1], self.order[0]
            dirs, route, dist = self.getRoute(gmaps, start, end)
            totalDistance += dist
            dist = str(round((int(dist)/float(conv)), 1))
            self.directionsText+="\nDirections from %s to %s \n" % (start, end)
            self.directionsText += "Total Distance: %s miles \n\n" % (dist)
            for step in route['Steps']:
                distance = str(round(step['Distance']['meters']/float(conv),
                                     1))+' miles'
                if distance == '0.0 miles':
                    distance = str(round(step['Distance']['meters']/float(conv)
                                         *conv2))+' feet'
                self.directionsText += (TSPSolver.strip_tags(
                    step['descriptionHtml']) + '\n' + distance + '\n')
        totalDistance = str(round(totalDistance/float(conv),1))
        self.directionsText += ("\nTotal Distance for Trip: %s miles\n"
                                % totalDistance)
        self.cleanDirectionsText()

    def cleanDirectionsText(self):
        #moves "Destination directions" to different line
        if self.directionsText != None:
            startIndex = 0
            while 'Destination' in self.directionsText[startIndex:]:
                index = self.directionsText.index('Destination', startIndex)
                self.directionsText = (self.directionsText[:index]+'\n'+
                                       self.directionsText[index:])
                offset = 3
                startIndex = index+offset
                
    def createListBoxText(self):
        #creates list box text for directions text
        xLength, yLength = 70, 33
        self.listbox = Listbox(self.root,width=xLength,height=yLength)
        xLoc, yLoc = 20, 20
        self.listbox.place(x=xLoc,y=yLoc)
        startIndex = 0
        while '\n' in self.directionsText[startIndex:]:
            newLineIndex = self.directionsText.index('\n',startIndex)
            self.listbox.insert(END,
                                self.directionsText[startIndex:newLineIndex])
            startIndex = newLineIndex+1

######################### Displaying Map in Web Browser ######################

    def getLatLng(self):
        #input address, returns lat, long coordinates of that address location
        gmaps = GoogleMaps()
        latLongList = []
        for address in self.order:
            start = address
            end = address
            dirs  = gmaps.directions(start, end)
            route = dirs['Directions']['Routes'][0]
            latLongList += [(str(route['Steps'][0]['Point']['coordinates'][1]),
                             str(route['Steps'][0]['Point']['coordinates'][0]))]
        return latLongList

    def makeMarkerLocHTML(self):
        #function that creates list of markers in format appropriate
        #for html file that displays map in web browser
        latLongList = self.getLatLng()
        markers = '['
        for i in xrange(len(self.order)):
            markers += '{'+"'title':"+"'"+str(self.order[i])+"'"+','
            markers += "'lat':"+"'"+str(latLongList[i][0])+"'"+','
            markers += "'lng':"+"'"+str(latLongList[i][1])+"'"+'}'
            if i != len(self.order)-1:
                markers += ','
        if self.startVar.get() == 1:
            markers += ','
            markers += '{'+"'title':"+"'"+str(self.order[0])+"'"+','
            markers += "'lat':"+"'"+str(latLongList[0][0])+"'"+','
            markers += "'lng':"+"'"+str(latLongList[0][1])+"'"+'}'
        markers += ']'
        return markers

    #readFile function taken from Professor Kosbie's notes
    @staticmethod
    def readFile(filename, mode="rt"):
        # rt = "read text"
        with open(filename, mode) as fin:
            return fin.read()
        
    #writeFile function taken from Professor Kosbie's notes
    @staticmethod
    def writeFile(filename, contents, mode="wt"):
        # wt = "write text"
        with open(filename, mode) as fout:
            fout.write(contents)

    def changeHTMLCode(self):
        #changes HTML code of basic framework to include cities put in
        #by the user, opens file with the map in webbrowswer
        markersList = self.makeMarkerLocHTML()
        contents = TSPSolver.readFile('testCreateHTMLMapworks copy.html')
        leftBracketIndex = contents.index('[')
        rightBracketIndex = contents.index(']')
        newContents = (contents[:leftBracketIndex] + markersList +
                    contents[rightBracketIndex+1:])
        #puts new marker locations where old markers were (between the [ ] in
        #the html file)
        TSPSolver.writeFile('testCreateHTMLMapworks copy.html',newContents)
        newFileName = ('file://'+
                       str(os.path.abspath('testCreateHTMLMapworks copy.html')))
        webbrowser.open_new_tab(newFileName)

################## Make Static Map for Canvas ################################

    def makeStaticMapURL(self):
        #returns url of map with markers referring to locations user inputted
        if len(self.citiesList) >= 1:
            width, height = 200, 200
            dmap = DecoratedMap(width,height)
            for index in xrange(len(self.citiesList)):
                dmap.add_marker(AddressMarker(self.citiesList[index],
                                              label=str(index+1)))
            self.readyToPutStaticMap = True
            return dmap.generate_url()

    def makeStaticImage(self):
        #draws static image of map containing locations user inputted
        #onto canvas
        if len(self.citiesList) >= 1:
            self.url = self.makeStaticMapURL()
            gifIndex = self.url.index('png')
            shift = 3
            self.url = self.url[:gifIndex]+'gif'+self.url[gifIndex+shift:]
            #converts png to gif file
            ReadImageFromWeb.run(self.canvas, self.url)

    ################# Button Functions ##############

    def buttonGetAddresses(self):
        #button for getting optimal order of addresses to visit
        self.buttonGetAddressesWidgetManager1()
        self.buttonGetAddressesWidgetManager2()
        def addAddressToList():
            self.addressAdder()
            self.createInputAddressBox()
            self.createOrderedAddressBox()
        if self.addAddressButton == None:
            self.addAddressButton = Button(text='Add Address',
                             command=addAddressToList)
            xLoc, yLoc = 430,540
            self.addAddressButton.place(x=xLoc,y=yLoc)
        self.buttonGetAddressesSetPageVariables()
        if len(self.citiesList) >= 2:
            self.readyToSolve = True
            distancesDict = copy.deepcopy(self.distancesDict)
            self.order = ([self.citiesList[0]]+
                          self.greedyAlgorithm(self.citiesList, distancesDict))
            self.readyToDrawOrder = True

    def buttonGetAddressesSetPageVariables(self):
        #sets page variables when user clicks address order button
        self.showAddressesPage = True
        self.showDemosPage = False
        self.showDirectionsText = False
        self.showAttractionsPage = False
        self.showSplashScreen = False
        self.showInstructionsPage = False

    def buttonGetAddressesWidgetManager1(self):
        #manages widgets for get Addresses page
        #destroys widgets when they shouldn't be displayed
        #creates widgets when they should be displayed
        if self.listbox != None:
            self.listbox.destroy()
            self.listbox = None
        if self.dropDownMenu != None:
            self.dropDownMenu.destroy()
            self.dropDownMenu = None
        if self.dropDownRadiusMenu != None:
            self.dropDownRadiusMenu.destroy()
            self.dropDownRadiusMenu = None
        if self.rentry != None:
            self.rentry.destroy()
            self.rentry = None
        if self.goButton != None:
            self.goButton.destroy()
            self.goButton = None

    def buttonGetAddressesWidgetManager2(self):
        #manages widgets for get Addresses page
        if self.getInfoButton != None:
            self.getInfoButton.destroy()
            self.getInfoButton = None
        if self.entry == None:
            self.createEntryBox()
        if self.infobox != None:
            self.infobox.destroy()
            self.infobox = None
        if self.finalDest == None:
            self.createFinalDestCheckBox()

    def buttonGetDirections(self):
        #button for displaying text based instructions on canvas
        if self.order != None:
            self.directionsText = ''
            self.showDirectionsText = True
            self.showDemosPage = False
            self.showAddressesPage = False
            self.showAttractionsPage = False
            self.showInstructionsPage = False
            self.getDirectionsText()
            self.buttonGetDirectionsWidgetManager()

    def buttonGetDirectionsWidgetManager(self):
        #manages widgets for get Directions page
        if self.listbox == None: self.createListBoxText()
        if self.finalDest != None:
            self.finalDest.destroy()
            self.finalDest = None
        if self.addAddressButton != None:
            self.addAddressButton.destroy()
            self.addAddressButton = None
        if self.dropDownRadiusMenu != None:
            self.dropDownRadiusMenu.destroy()
            self.dropDownRadiusMenu = None
        if self.infobox != None:
            self.infobox.destroy()
            self.infobox = None
        if self.addressInputBox != None:
            self.addressInputBox.destroy()
            self.addressInputBox = None
        if self.dropDownMenu != None:
            self.dropDownMenu.destroy()
            self.dropDownMenu = None

    def buttonGetMap(self):
        #button for opening map displaying visual route to user in
        #web browser
        if self.order != None:
            self.changeHTMLCode()
            self.changeHTMLCode()
            
    def buttonDemos(self):
        #button for showing the TSP algorithm demos
        self.startingLoc = None
        self.readyToDrawLines = False
        if self.order != None:
            self.buttonDemosWidgetManager1()
            self.buttonDemosWidgetManager2()
            self.showDemosPage = True
            self.showDirectionsText = False
            self.showAddressesPage = False
            self.showAttractionsPage = False
            self.showInstructionsPage = False
            if len(self.citiesList) >= 1:
                self.url = self.makeStaticMapURL()
                gifIndex = self.url.index('png')
                shift = 3
                self.url = self.url[:gifIndex]+'gif'+self.url[gifIndex+shift:]
                #convirt to gif image
                self.translateActualMarkerCoords()
                self.removeNearbyPoints()
                self.getDistancesBetweenMarkers(self.actualMarkerCoords)
                self.readyToDoReadyAlg = True

    def buttonDemosWidgetManager1(self):
        #manages widgets for TSP demos page
        if self.addAddressButton != None:
            self.addAddressButton.destroy()
            self.addAddressButton = None
        if self.addressInputBox != None:
            self.addressInputBox.destroy()
            self.addressInputBox = None
        if self.orderedAddressesBox != None:
            self.orderedAddressesBox.destroy()
            self.orderedAddressesBox.destroy()
        if self.dropDownRadiusMenu != None:
            self.dropDownRadiusMenu.destroy()
            self.dropDownRadiusMenu = None
        if self.listbox != None:
            self.listbox.destroy()
            self.listbox = None
        if self.entry != None:
            self.entry.destroy()
            self.entry = None

    def buttonDemosWidgetManager2(self):
        #manages widgets for TSP demos page
        if self.rentry != None:
            self.rentry.destroy()
            self.rentry = None
        if self.goButton != None:
            self.goButton.destroy()
            self.goButton = None
        if self.getInfoButton != None:
            self.getInfoButton.destroy()
            self.getInfoButton = None
        if self.dropDownMenu != None:
            self.dropDownMenu.destroy()
            self.dropDownMenu = None
        if self.infobox != None:
            self.infobox.destroy()
            self.infobox = None
        if self.finalDest != None:
            self.finalDest.destroy()
            self.finalDest = None

    def buttonAttractions(self):
        #button for finding nearby gas stations to locations on trip
        if self.order != None:
            self.showAttractionsPage = True
            self.showDemosPage = False
            self.showDirectionsText = False
            self.showAddressesPage = False
            self.showInstructionsPage = False
            self.makeDropDownMenu()
            self.makeDropDownRadiusMenu()
            self.createGoButton()
            self.createGetInfoButton()
            self.buttonAttractionsWidgetManager()

    def buttonAttractionsWidgetManager(self):
        #manages widgets for attractions page
        if self.listbox != None:
            self.listbox.destroy()
            self.listbox = None
        if self.entry != None:
            self.entry.destroy()
            self.entry = None
        self.buttonAttractionsWidgetManager2()
        xLoc, yLoc = 350, 470
        self.createInputAddressBox(xLoc,yLoc)

    def buttonAttractionsWidgetManager2(self):
        #manages widgets for attractions page
        if self.addAddressButton != None:
            self.addAddressButton.destroy()
            self.addAddressButton = None
        if self.addressInputBox != None:
            self.addressInputBox.destroy()
            self.addressInputBox = None
        if self.orderedAddressesBox != None:
            self.orderedAddressesBox.destroy()
            self.orderedAddressesBox = None
        if self.finalDest != None:
            self.finalDest.destroy()
            self.finalDest = None

    def buttonInstructions(self):
        #button for showing instructions page
        self.showInstructionsPage = True
        self.showAttractionsPage = False
        self.showDemosPage = False
        self.showDirectionsText = False
        self.showAddressesPage = False
        self.buttonInstructionsWidgetManager1()
        self.buttonInstructionsWidgetManager2()

    def buttonInstructionsWidgetManager1(self):
        #manages widgets for instructions page
        if self.listbox != None:
            self.listbox.destroy()
            self.listbox = None
        if self.entry != None:
            self.entry.destroy()
            self.entry = None
        if self.finalDest != None:
            self.finalDest.destroy()
            self.finalDest = None
        if self.addAddressButton != None:
            self.addAddressButton.destroy()
            self.addAddressButton = None
        if self.addressInputBox != None:
            self.addressInputBox.destroy()
            self.addressInputBox = None
        if self.orderedAddressesBox != None:
            self.orderedAddressesBox.destroy()
            self.orderedAddressesBox = None

    def buttonInstructionsWidgetManager2(self):
        #manages widgets for instructions page
        if self.dropDownMenu != None:
            self.dropDownMenu.destroy()
            self.dropDownMenu = None
        if self.dropDownRadiusMenu != None:
            self.dropDownRadiusMenu.destroy()
            self.dropDownRadiusMenu = None
        if self.getInfoButton != None:
            self.getInfoButton.destroy()
            self.getInfoButton = None
        if self.goButton != None:
            self.goButton.destroy()
            self.goButton = None
        if self.infobox != None:
            self.infobox.destroy()
            self.infobox = None

########################### Find Nearby Attractions Page #####################

    def makeDropDownMenu(self):
        #creates drop down menu widget listing chosen addresses
        if len(self.citiesList) >= 2 and self.dropDownMenu == None:
            self.addressSelected = StringVar(self.root)
            self.addressSelected.set("Addresses")
            self.dropDownMenu=apply(OptionMenu,(self.root,self.addressSelected)
                                    +tuple(self.citiesList))
            xLoc = 440
            yLoc = 10
            self.dropDownMenu.place(x=xLoc,y=yLoc, anchor=NW)

    def makeDropDownRadiusMenu(self):
        #creates drop down menu widget for choice of radii
        radiusList = [0.5,1.0,1.5,2.0]
        if len(self.citiesList) >= 2 and self.dropDownRadiusMenu == None:
            self.radiusSelected = StringVar(self.root)
            self.radiusSelected.set("Radius (miles)")
            self.dropDownRadiusMenu = apply(OptionMenu,
                                            (self.root,self.radiusSelected)+
                                            tuple(radiusList))
            xLoc = 438
            yLoc = 330
            self.dropDownRadiusMenu.place(x=xLoc,y=yLoc, anchor=SW)

    def createGoButton(self):
        #creates "Go Button" widget to find nearby gas stations
        numPair = 2
        if len(self.citiesList) >= numPair:
            def getGasStations():
                if (self.addressSelected.get() != 'Addresses' and
                    self.radiusSelected.get() != "Radius (miles)"):
                    self.findNearbyAttractions(float(self.radiusSelected.get()),
                                               self.addressSelected.get())
                    self.readyToDrawAttractionsMap = True
            if self.goButton == None:
                xLoc = 440
                yLoc = 380
                self.goButton = Button(text='Go!',command=getGasStations)
                self.goButton.place(x=xLoc,y=yLoc, anchor = SW)

    def createGetInfoButton(self):
        #creates "Get Info button" widget to get info on nearby gas stations
        if len(self.citiesList) >= 2:
            def getInfo():
                if self.mapCityToLatLong != None:
                    self.placesInfoBox()
            if self.getInfoButton == None:
                xLoc = 440
                yLoc = 430
                self.getInfoButton=Button(text = "Get Info", command=getInfo)
                self.getInfoButton.place(x=xLoc,y=yLoc, anchor = SW)

    def findNearbyAttractions(self, r, loc):
        #takes in radius and location (center),finds all gas stations within the
        #specified radius from the location
        if loc != "Addresses":
            self.loc = loc
            mapCityToLatLong = dict()
            YOUR_API_KEY = 'AIzaSyBrDq_8ZKnBgqKW9x30gw5PgaggyM_Ta2M'
            r *= 1609.34
            #convert input radius in miles to meters (to work with API)
            google_places = GooglePlaces(YOUR_API_KEY)
            query_result = google_places.nearby_search(
                    location=loc,
                    radius=r, types=[types.TYPE_GAS_STATION])
            for place in query_result.places:
                place.get_details()
                mapCityToLatLong[place.name]=(place.geo_location['lat'],
                                              place.geo_location['lng'],
                                              place.details['vicinity'])
            self.mapCityToLatLong = mapCityToLatLong
            return mapCityToLatLong

    def createAttractionsMapURL(self, loc):
        #takes in a location, adds it as a marker, returns the url for
        #the map centered around the location with all nearby gas stations
        mapCityToLatLong = self.mapCityToLatLong
        mapWidth = mapHeight = 200
        dmap = DecoratedMap(mapWidth,mapHeight)
        dmap.add_marker(AddressMarker(loc,label='A'))
        count = 0
        maxCities = 9
        for city in mapCityToLatLong:
            count += 1
            dmap.add_marker(LatLonMarker(mapCityToLatLong[city][0],
                                         mapCityToLatLong[city][1],
                                         color='blue',
                                         label = str(count)))
            if count == maxCities:
                break #do not include more than 9 gas stations
        self.showAttractionsURL = dmap.generate_url()
        return dmap.generate_url()

    def makeStaticImage2(self):
        #draws static image of map containing locations user inputted
        #onto canvas
        if len(self.citiesList) >= 1:
            self.showAttractionsURL = self.createAttractionsMapURL(self.loc)
            gifIndex = self.showAttractionsURL.index('png')
            self.showAttractionsURL = (self.showAttractionsURL[:gifIndex]+'gif'
                                       +self.showAttractionsURL[gifIndex+3:])
            #convert png to gif image
            ReadImageFromWeb2.run(self.canvas, self.showAttractionsURL)

    def selection(self, event):
        #function that on double click, allows user to add gas station
        #address to list of addresses he wants to visit
        self.isThereGasStationError = False
        address = self.infobox.get(ACTIVE)
        startI = 9
        if address[0] == 'A' and address[startI:] not in self.citiesList:
            try:
                self.distancesDict = self.getDistances(address[startI:],
                                                   self.citiesList,
                                                   self.distancesDict)
                self.citiesList += [address[startI:]]
            except Exception as err:
                self.isThereGasStationError = True
                self.gasStationError = "Unknown Gas Station Address"
        xLoc, yLoc = 350, 470
        self.createInputAddressBox(xLoc,yLoc)

    def placesInfoBox(self):
        #creates places info entry box widget
        if self.infobox != None:
            self.infobox.destroy()
            self.infobox = None
        #if widget were already there, destroy it and create a new one
        listBoxWidth, listBoxHeight = 30, 10
        self.infobox=Listbox(self.root,width=listBoxWidth,height=listBoxHeight)
        self.infobox.bind("<Double-Button-1>", self.selection)
        xLoc, yLoc = 50, 430
        self.infobox.place(x=xLoc,y=yLoc)
        startIndex = 0
        count = 1
        addressIndex = 2
        maxCityNum = 10
        for city in self.mapCityToLatLong:
            self.infobox.insert(END, str(count)+'. '+
                                city)
            self.infobox.insert(END, "Address: " +
                                self.mapCityToLatLong[city][addressIndex])
            count += 1
            if count == maxCityNum:
                break 

########### Find coordinates of markers on static map ########################

    #below function taken from Professor Kosbie's notes on steganography
    def getRGB(self, image, x, y):
        #gets RGB triple of the point (x,y) on the image
        value = image.get(x, y)
        return tuple(map(int, value.split(" ")))

    def findMarkerLocations(self,image):
        #finds possible coordinates where markers are located in image
        #according to rgb values of the pixels
        image = PhotoImage(file=image)
        possMarkerCoords = []
        for x in xrange(image.width()):
            for y in xrange(image.height()):
                (r, g, b) = self.getRGB(image, x, y)
                rUpper, rLower, gUpper, bUpper = 195, 180, 70, 70
                if rUpper > r > rLower and g < gUpper and b < bUpper:
                    possMarkerCoords += [(x,y)]
        #if the pixel has large r-value, small g,b-values, it must be a marker
        return possMarkerCoords

    def retrieveMapFromURL(self, url):
        #takes in url string, retrieves image
        #& stores it in 'mapWithLocations.gif' file
        urllib.urlretrieve(url,'mapWithLocations.gif')

    def getMarkerCoords(self):
        #gets possible marker coordinates from image stored in
        #'mapWithLocations.gif
        self.retrieveMapFromURL(self.url)
        possMarkerCoords = self.findMarkerLocations('mapWithLocations.gif')
        return possMarkerCoords

    def separateMarkerCoords(self):
        #separates marker coordinates into groups
        #corresponding to different markers
        possMarkerCoords = self.getMarkerCoords()
        output = [] #2d list containing groups of points with similar
        #(x,y) coordinates - each group corresponds to a unique marker
        for coord1 in possMarkerCoords:
            if output == []:
                output += [[coord1]] #add coordinate to a new group
            else:
                output = self.findSimilarGroup(output,coord1)
        return output

    def findSimilarGroup(self, output, coord1):
        #puts the next possible coordinate into a previous group if it "fits",
        #else, puts coordinate into new group
        mWidth = 17
        mHeight = 36 #marker width, height
        for groupIndex in xrange(len(output)):
            brokenLoop = False
            for coord2Index in xrange(len(output[groupIndex])):
                if (abs(coord1[0]-output[groupIndex][coord2Index][0])>mWidth or
                    abs(coord1[1]-output[groupIndex][coord2Index][1])>mHeight):
                    brokenLoop = True
                    break
            #if the new coordinate is more than 1 marker width or length away
            #from any previous point in the group, it doesn't belong
            if brokenLoop == False: #add the coordinate to the group (it fits)
                output[groupIndex] += [coord1]
                return output
        output += [[coord1]] #add the coordinate to a new group
        return output

    def findRepresentativePoint(self):
        #takes in a list "grouped" according to markers, returns
        #a list of representative points (one for each marker)
        groupedList = self.separateMarkerCoords()
        representativePoints = []
        for group in groupedList:
            representativePoints += [max(group)]
            #take the point with the max x-coordinate (to be consistent)
        return representativePoints

    def translateActualMarkerCoords(self):
        #translates all coordinates to their actual locations on the canvas
        #(approximately, the midpoint of the marker)
        newMarkerCoords = self.findRepresentativePoint()
        actualMarkerCoords = []
        mapX, mapY = 100, 100
        #(100,100) - coordinates of top-left point on map
        transX, transY = -8, 10
        zoomFactor = 2
        for coord in newMarkerCoords:
            newCoord = (mapX+zoomFactor*(coord[0]+transX),
                        mapY+zoomFactor*(coord[1]+transY))
            actualMarkerCoords += [newCoord]
        self.actualMarkerCoords = actualMarkerCoords

    def removeNearbyPoints(self):
        #if some coordinates are very close together, function removes
        #all but 1 coordinate (representative coordinate in a "region")
        threshold = 30
        #if markers points are within 30 of each other, they are too close
        finalCoords = []
        for coord1 in self.actualMarkerCoords:
            tooClose = False
            coord1Index = self.actualMarkerCoords.index(coord1)
            for coord2 in self.actualMarkerCoords[coord1Index+1:]:
                dist = round(math.sqrt((coord1[0]-coord2[0])**2 +
                                       (coord1[1]-coord2[1])**2), 1)
                if dist <= threshold:
                    tooClose = True
            if tooClose == False: #keep the point
                finalCoords += [coord1]
        self.actualMarkerCoords = finalCoords              

############ Perform TSP Greedy Algorithm on "Marker Points" #################

    def getDistancesBetweenMarkers(self,listOfCoords,
                                   distances={}):
        #recursively get linear distance between every representative point
        #in the list of marker coordinates
        listOfCoords = copy.copy(listOfCoords)
        if len(listOfCoords) == 1:
            return distances
        for coord in listOfCoords[1:]:
            distance = round(math.sqrt((listOfCoords[0][0]-coord[0])**2 +
                                 (listOfCoords[0][1]-coord[1])**2),1)
            distances[listOfCoords[0],coord] = distance
        return self.getDistancesBetweenMarkers(listOfCoords[1:]
                                          ,distances)
                    
    def greedyAlgModified(self, selectedList, distancesDict):
        #recursivly applies TSP greedy algorithm to find optimal
        #order of addresses to visit (according to distance)
        if len(selectedList) == 1: return []
        minDistance, minPoint, cityPair = None, None, None
        for pair in distancesDict:
            if selectedList[0] in pair:
                if (distancesDict[pair] < minDistance or
                    minDistance == None):
                    minDistance = distancesDict[pair]
                    cityPair = pair
                    if selectedList[0] != pair[0]: minPoint = pair[0]
                    else: minPoint = pair[1]
        #find the closest point of the remaining points
        pairsToDelete = []
        for pair in distancesDict:
            if pair[0] == selectedList[0] or pair[1] == selectedList[0]:
                pairsToDelete += [pair]
        for pair in pairsToDelete: del distancesDict[pair]
        #delete all keys with previous point (no going back in Greedy Alg)
        #the next point becomes the starting point
        i = selectedList.index(minPoint)
        selectedList = [minPoint] + selectedList[1:i] + selectedList[i+1:]
        return [minPoint]+self.greedyAlgModified(selectedList,
                                                 distancesDict)

    def greedyAlgorithmDemo(self):
        #finds optimal order to visit markers according to TSP Greedy Algorithm
        if self.startingLoc != None:
            markerCoords = copy.copy(self.actualMarkerCoords)
            distances = self.getDistancesBetweenMarkers(markerCoords,{})
            startingLocIndex = self.actualMarkerCoords.index(self.startingLoc)
            revisedMarkerList = ([self.actualMarkerCoords[startingLocIndex]] +
                                 self.actualMarkerCoords[:startingLocIndex]+
                                 self.actualMarkerCoords[startingLocIndex+1:])
            self.orderToVisitDemo=([revisedMarkerList[0]]+
                                   self.greedyAlgModified(revisedMarkerList,
                                                          distances))

TSPSolver().run()


##############################################################################
#############################Test Functions###################################
##############################################################################

class TestClass(TSPSolver):
    
    @staticmethod
    def almostEqual(a,b):
        return abs(a-b) < 10**(-2)

    def testDist(self):
        print "Testing dist(self, a, b)...",
        assert TestClass.almostEqual(self.dist((1,2),(3,4)),2.82)
        assert TestClass.almostEqual(self.dist((5,3),(8,10)), 7.62)
        assert TestClass.almostEqual(self.dist((0,0,),(4,0)), 4)
        print "Passed"

    def testFindTotalTwoOptDistance(self):
        print "Testing findTotalTwoOptAlgDist(self, selectedList)",
        assert (self.findTotalTwoOptAlgDist([(0,0),(8,9),(5,3)])
                == [0, 12.0, 18.7, 24.5])
        assert (self.findTotalTwoOptAlgDist([(-1,4),(4,8),(12,3),(7,4),
                                     (8,4)]) ==
               [0, 6.4, 15.8, 20.9, 21.9, 30.9])
        assert (self.findTotalTwoOptAlgDist([(0,0)]) == [0, 0.0, 0.0])
        print "Passed"

    def testFindClosestPoint(self):
        print "Testing findClosestPoint(self, selectedList)",
        assert (self.findClosestPoint([(0,0),(8,9),(5,3)]) ==
                [(0, 0), (5, 3), (8, 9)])
        assert (self.findClosestPoint([(-1,4),(4,8),(12,3),(7,4),
                                     (8,4)]) ==
                [(-1, 4), (4, 8), (7, 4), (8, 4), (12, 3)])
        assert (self.findClosestPoint([(0,0)]) == [(0, 0)])
        print "Passed!"

    def testTwoOptAlg(self):
        print "Testing twoOptAlg(self, pointList)...",
        assert (self.twoOptAlg([(0,0),(8,9),(5,3)]) ==
               [(0, 0), (8, 9), (5, 3)])
        assert (self.twoOptAlg([(0,0),(8,9),(5,3),(1,5),(9,8),
                               (10,10),(4,5)]) ==
               [(0, 0), (1, 5), (4, 5), (8, 9), (10, 10), (9, 8), (5, 3)])
        assert (self.twoOptAlg([(0,0)]) == [(0,0)])
        print "Passed!"

    def testRemoveNearbyPoints(self):
        print "Testing removeNearbyPoints(self)",
        self.actualMarkerCoords = [(0,0),(8,9),(5,3)]
        self.removeNearbyPoints()
        assert(self.actualMarkerCoords == [(5, 3)])
        self.actualMarkerCoords = [(-1,4),(4,8),(12,3),(7,4),
                                     (8,4)]
        self.removeNearbyPoints()
        assert(self.actualMarkerCoords == [(8, 4)])
        self.actualMarkerCoords = [(0,0),(1,1)]
        self.removeNearbyPoints()
        assert(self.actualMarkerCoords == [(1, 1)])
        print "Passed!"

def testAll():
    tester = TestClass()
    tester.testDist()
    tester.testFindTotalTwoOptDistance()
    tester.testFindClosestPoint()
    tester.testTwoOptAlg()
    tester.testRemoveNearbyPoints()

#testAll()
