# Strava Dog Explorer
![screenshot](https://github.com/BenVanCitters/stravaDogExplorer/blob/master/Screen%20Shot%202022-06-21%20at%202.03.56%20AM.png)

This is simple app uses MapBox and Strava to display a map with the last two weeks of dog walk activities (which I studiously record alongside my faithful woofer, Isaac) all at once to help inspire me vary the routes we walk.

To use the web-app you will need a few things:
1. The ability to run Python and flask
2. The ability to log in to strava so you can provide authorization for my strava webapp to connect to your strava account so that it can access your walks
3. From 2, the client id and secret to retrieve strava walk data saved in 'clientinfo.json' at the root directory

Once you have all of that all you have to do is run the command  
```./runDogStrav```  
from the git directory to initialize flask

Once flask is running visit:  
[https://localhost:5000](https://localhost:5000)  
ad you should see you most recent 2 weeks of walks!

To make this sketch there is a strava app which makes the activites available on a athlete by athlete basis.  The flask python app pulls that data down and pushes it on to a mapbox map via geojson layers.
