

# Arent Test - SF Movies

1. [Problem](#prob)
    1. [Description](#prob-description)
    2. [Challenges](#prob-challenges)

2. [Solution](#sol)
    1. [Description](#sol-description)
    2. [Modivations of Choices](#sol-motivation)
    3. [Discussion](#sol-discussion)
    4. [Automation Testing](#sol-automation-testing)
    5. [Enhancement](#sol-enhancement)


## 1. Problem <a id='prob'></a>
### 1.1. Description <a id='prob-description'></a>
Build a service in order to show movies filmed in San Francisco on map. The user is able to filter the view using autocomplete search.

### 1.2. Challenges <a id='prob-challenges'></a>
The provided dataset is not including 2 important attributes, which are Latitude and Longitude, in order to show markers of these movies' location on the map. This leads to get the coordinates by sending requests to online map supplier, in this solution I am using APIs called [Nominatim](https://nominatim.openstreetmap.org/ui/search.html) from [OpenStreetMap](https://www.openstreetmap.org).

To get the coordinates by calling the APIs, we have to apply the location of filmed movie into query URL. So, we need to process these locations before sending requests. This is a difficult task because we have to get the coordinates as many as possible. We will use these coordinates to show marker of movies on the map.

During fetching the coordinates to create coordinates CSV file, it takes long time to send and revieve response from Nominatim, though there are just 2000 records in dataset. So when the records number increases in the future, we will need more time to send query URL and save the coordinates into a dataset file such as CSV. The coordinates CSV file is created when the server is started but there's no coordinates CSV file.

## 2. Solution <a id='sol'></a>
### 2.1. Description <a id="sol-description"></a>
Solution focuses on back - end. At first, we process the movies' location before sending query URL to Nominatim. 
After getting the needed coordinates, we must save these so I created a new CSV file which contains the base attributes of provided dataset and 2 new attributes Latitude and Longitude.

### 2.2. Movivations of Choices <a id="sol-motivation"></a>
Nguyên do đưa ra giải pháp

### 2.3. Discussion <a id="sol-discussion"></a>
Đánh đổi những gì

### 2.4. Automation Testing <a id='sol-automation-testing'></a>
https://flask.palletsprojects.com/en/2.0.x/testing/

```
py -m unittest discover
```

<!-- ## 3. Hồ sơ của tôi -->