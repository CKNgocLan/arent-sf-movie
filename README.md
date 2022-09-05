

# Arent Test - SF Movies

1. [Problem](#prob)
    1. [Description](#prob-description)
    2. [Challenges](#prob-challenges)

2. [Solution](#sol)
    1. [Description](#sol-description)
    2. [Motivations of Technical Choices](#sol-motivation)
    3. [Discussion and Enhancement](#sol-discussion-enhancement)


## 1. Problem <a id='prob'></a>
### 1.1. Description <a id='prob-description'></a>
Build a service in order to show movies filmed in San Francisco on map. The user is able to filter the view using autocomplete search.

### 1.2. Challenges <a id='prob-challenges'></a>
The provided dataset is not including 2 important attributes, which are Latitude and Longitude, in order to show markers of these movies' location on the map. This leads to get the coordinates by sending requests to online map supplier, in this solution I am using APIs called [Nominatim](https://nominatim.openstreetmap.org/ui/search.html) from [OpenStreetMap](https://www.openstreetmap.org).

To get the coordinates by calling the APIs, we have to apply the location of filmed movie into query URL. So, we need to process these locations before sending requests. This is a difficult task because we have to get the coordinates as many as possible. We will use these coordinates to show marker of movies on the map.

During fetching the coordinates to create coordinates CSV file, it takes long time to send and revieve response from Nominatim, though there are just 2000 records in dataset. So when the records number increases in the future, we will need more time to send query URL and save the coordinates into a dataset file such as CSV. The coordinates CSV file is created when the server is started but there's no coordinates CSV file.

## 2. Solution <a id='sol'></a>
### 2.1. Description <a id="sol-description"></a>
Solution focuses on back-end. At first, we process the movies' location before sending query URL to Nominatim. After getting the needed coordinates, we have to save these so I created a new CSV file which contains the base attributes of provided dataset and 2 new attributes Latitude and Longitude. Then we pass the received coordinate values from server side to client side, in this client side, we will create markers with [Leaflet](https://leafletjs.com/) (a Javascript library for interactive map) and show on the map.

On the screen we are showing to user, I have add an autocomplete search input. When the user fill in with some values of movies' title, a dropdown list of movie titles will be showed so that the user can choose one and the markers of choosen movie's locations will be re-displayed according to choose movie.

### 2.2. Motivations of Technical Choices <a id="sol-motivation"></a>
Because we have to do some analysis on the location values, I decided to use Python for back-end due to advantages of analysis from this high-level language. And the client screen does not require complex technology or functionalities, so I decided to use [Flask](https://flask.palletsprojects.com/en/2.2.x/) (Flask is a web application framework written in Python and developed by Armin Ronacher).

With Flask, we can build simple back-end for the user to process Get or Post request and simple front-end for the user by combining Bootstrap.

### 2.3. Discussion and Enhancement <a id="sol-discussion-enhancement"></a>
We have to create coordinate CSV file so it will take time when there's no coordinates file. Be default, after starting server and no coordinate file, when the first request to root endpoint received, the system is going to create coordinate CSV file. This needs long time to process the first request so it's necessary to warn that the user will wait for long time.

There are still movies' location not showed on the map so we have to improve the process that transforms location before applying to query URL if we want more movies' location showed accurately.

Spent Time:

|   Date        |   Time|
|:-------------:|------:|
|	24/08/2022	|	3	|
|	25/08/2022	|	2	|
|	26/08/2022	|	0	|
|	29/08/2022	|	0.5	|
|	01/09/2022	|	3.5	|
|	02/09/2022	|	2	|
