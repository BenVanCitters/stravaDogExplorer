# Strava Dog Explorer
Simple app I made connecting strava activities on to a mapbox map.

The app uses MapBox and Strava to display a map with the last two weeks of dog walks (which I studiously record alongside my faithful woofer, Isaac) all at once to help inspire me vary the routes we walk.

To use the web-app you will need a few things:
1. The ability to run Python and flask
2. The ability to log in to strava so you can provide authorization for my strava webapp to connect to your strava account so that it can access your walks
3. From 2, the client id and secret to retrieve strava walk data saved in 'clientinfo.json' at the root directory

Once you have all of that all you have to do is run the command 
./runDogStrav
from the git directory to initialize flask

Once flask is running visit:
localhost:5000
ad you should see you most recent 2 weeks of walks!

To make this sketch there is a strava app which makes the activites available on a athlete by athlete basis.  The flask python app pulls that data down and pushes it on to a mapbox map via geojson layers.
