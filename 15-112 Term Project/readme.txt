Project Readme File

###########################################################################
Project Description

In this project, I have created a program that implements the Traveling Salesman Problem (TSP) Greedy Algorithm to provide an optimal round-trip path through a series of locations (addresses) entered by the user. 

The program will generate the optimal order in which to visit the addresses according to the greedy algorithm. It will provide text-based driving instructions (from Google Maps API) of how to travel through each stage in the route. Additionally, the program will display a visual depiction of the route on a scrollable/zoomable map in the user’s web browser (also through Google Maps API). 

Moreover, the user can choose any location in his current route and request for gas stations within a specified radius from the location. The program will then add the selected gas station into the user’s route and recompute the optimal order in which to visit the addresses inputted by the user.

The user can also view a simulation of the traveling salesman algorithm applied to the specific locations he inputted. The simulation is overlaid on a map with nodes corresponding to actual locations entered.

###########################################################################
How to run this project

To run this project, one will need the following modules: eventBasedAnimationClass2 (slightly modified Professor Kosbie’s version),
googlemaps.py (Google Maps API wrapper for python), motionless.py (Static Maps API wrapper for python), and googleplaces.py (Google Places API). 

In my submission, I have included all the above modules, so simply run the NewTermProjectFinalUltimateSubmission.py file.
