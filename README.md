# WEATHER FRONT
#### Video Demo:  <URL https://youtu.be/c2SZw5-FB8c>
#### Description:
Weather front is a webpage containing weather data and weather forecasts for cities all around the world. The project was created using the following technologies:
- Python with flask (accessing weather data of openweathermap.com through API keys)
- SQL Lite
- Html
- Bootstrap
- CSS

HOW THE WEBPAGE IS USED - in short

The index page of the webpage prompts the user to search for a certain city. In the navigation bar, there are options "Login" and "Register". When the user enters a certain city, there is a list displayed on the webpage showing names (links) of cities that are similar to the one searched. If there are no matches, an apology appears. When a certain link is clicked, basic weather data is displayed for that city (current conditions, maximum and minimum temperature, wind direction, pressure etc.)
To get more detailed data about weather, the user has to register. On the register page, the user is prompted to enter a username, password and confirmation of the password. To log in, the user needs to enter his/her username and password. When logged in, the user can use the same procedure as mentioned before to find weather data for a given city. Now the weather information is displayed in more detail (besides basic information, there is also a 5-day forecast containing date and name of the day with an icon showing weather expected for the given day and also maximum and minimum temperatures in degrees Celsius). For each day, there is an option to view temperatures and conditions hourly (in 3-hour spans). The hourly forecast shows the temperature and an icon (sunny, cloudy, mist etc.) for each time of the day. There is also an option to add the city to favorites. That means that that city will be saved and displayed on "My favorites" page as a link in a list. Multiple cities can be added and removed from the list. You can access that city by clicking on the name (the link). "My favorites" page can be accessed through the navigation bar. Also, logging out can always be done through the navigation bar in the right corner.

HOW EACH INDIVIDUAL FILE WORKS

app.py

The fille app.py starts with importing certain libraries used (SQL from cs50, flask, password hash from werkzeug.security, defaultdict from collections and datetime from datetime). Before the main functions, there are lines of code the same as from the "Finance" problem set that take care of configuring the application and configuring the session to use file system and configuring the CS50 library to use the SQL database.
Function index has a GET and a POST method, if the GET method is used, the function renders the template "index-html" (home page). If the POST method is used, that means that the user has searched for a city. To search for a city, a helper function called search is used. If there is at least one city found in the database, the results are then passed to rendering the page "search_result.html" and displayed on it in a list fashion. If no results are found, an apology is rendered.


Function city takes one argument (the city name that is clicked on on a list of cities found). It begins with defining a global variable (so that it can later be used by other functions) and assigning it the name of the current city that was clicked on. Then it uses a helper function "lookup" to search for weather data through an API key of openweathermap. Particular info of the forecast is divided into two variables (urli and forecast and passed to "weatherlim.html" for rendering).

Function hourly takes care of selecting proper inormation to be displayed in terms of 3-hour forecast for a certain day of the 5-day forecast. The variable name1 is defined as the city name that was last clicked on and the day is defined as the date that was clicked on on the page "weatherlim.html".  It again uses the lookup function to find the forecast data and all 3-hour forecasts are saved in a dictionary of lists. It also uses datetime library to convert text info to a readable format of time. All the info is then passed to the page "hourly.html" and the page gets rendered.


Function favorites takes no arguments. When "My favorites" is clicked in the navigation bar, the function favorites checks the SQL database for favorite cities for the user currently signed in. If it returns no data, an apology gets rendered. If the table contains data of favorites, a string gets split by ";" and gets passed into a list, so that all favorite city names are separated. Then it gets passed to "favorites.html" for rendering.

Function add_favorites selects favorite column from the users table in the SQL file and the info gets passed to the variable intro. If the variable equals None (the data on favorites is empty), the global variable name1 is now the value of intro, meaning the current city gets to be the only favorite city. If there are already city names in the favorite column, the current city name gets added, each name separateb by ";". If the current city is already in the favorites, an apology gets rendered.

Function remove_favorites is designed to remove a city name from the favorites list. As in the previous function, data of the existing favorite cities gets passed from the SQL database to a variable "favorites_names" and gets split into a list. From that list, the city which the user wants  to remove, gets removed. And then the SQL gets updated with the new variable.

Functions login, logout and register are essentially the same as the ones in the Problem set 9 - Finance, so I will not bother explaining them.

helpers.py

Functions apology and login_required are also essentially the same as in the project Finance.

Function degrees is meant to convert data that gets passed from using the API key of wind direction in degrees to actual symbols of wind direction. A dictionary of lists contains wind direction symbols and their responding values in degrees. If the value that gets passed to the function is between a certain span of degrees, the key (direction symbol) gets returned.

A helper function called search gets passed one argument (city). First of all it makes sure the API key is set, then it passes information into a dictionary named params so that is in the proper form for using the API key. A request gets sent to openweathermap with the find endpoint. The response gets stored in the json format. A loop runs through the returned list of cities and info about the name and the county gets appended to a new list. The function then returns this new list.

Similar to the search function, the lookup function first makes sure the API key is set, then it stores the info of the passed argument in a dictionary. A request gets sent to openweathermap via the weather endpoint and if it is successful, the response gets stored in json format. Weather information gets stored in separate variables (description, icon, link, temperature etc.). To retrieve this info from the json format, indexing is used.
To retrieve forecast information, another request gets sent to openweathermap, this time via the endpoint forecast and the successful response is stored in json format. A for loop gets run through the list that is returned. First, the current date is defined in the variable today. Then the date and weekday for each forecast are defined or reformatted using the datetime function and are then combined into a string. If the date of the forecast happens to be today, it gets passed, because we don't want to show today's forecast, it is already displayed. Future forecasts are then saved in a dictionary of lists for each individual day.
A for loop gets run through the new dictionary of lists (forecasts_by_day). Firstly, min and max temperatures are defined as positive and negative values, also icon_12 variable is defined as None. Then a loop runs through the list of a specific daytime information and the currently defined minimum temperature gets compared to the one in the current daytime. If the second is smaller, it gets assigned as the new minimum temperature. The same goes for the maximum temperature. The responding icon for each day is the icon that is predicted for 12:00:00 daytime in each day. When the for loop is finished, the three values (min_temp, max_temp and icon_12) get passed to a dictionary daily_brief. This dictionary getss apended to the end of the list of weather information for each given day of the forecast.
The function then returns a dictionary containing keys with  their responding values that we wish to display as weather information. If any of the requests aren't successful, the function returns None.

weather.db

weather.db is an SQL datatbase file that contains information about users (their id, username, hashed password and favorite cities).

static directory
favicon.ico - contains an icon or an image of a sun and clouds that gets displayed on the tab where the weather page is open.
styles.css - contains styles for certain elements displayed on the webpage (size and color for the navigation bar brand, size for the custom-input class, padding and color for table headings and table data elements, background image of each html body element, display styles of button groups, navigation bar background color and primary button colors.)
image directory - contains an image element "25503.jpg". This is the backgrond image of the basic layout.

templates directory

apology.html - this html file is essentially very similar to the one used in Finance. The changes were made in the text that gets displayed when an apology is rendered ("SORRY") and the image is now new, displaying a customer service employee for more sophisticated and user-friendly experience.

favorites.html - favorites_list variable gets passed to this template from the function favorites. A for loop runs through this list and for each city name, one link gets displayed with the responding city name, and for each element in the list, a remove button is displayed.

hourly.html - an h4 title is displayed for the responding day, the information gets passed from the hourly function in app.py. there are three for loops running through a dictionary of all datytimes, displaying time of the day, a weather description responding icon and the temperature. The information is displayed in a table fashion.

index.html - firstly it contains a style element that takes care of color styles for words displayed in the search button. Then, within a form element, an input element lies where the user enters a city name. An if statement takes care of what kind of search button gets displayed to the user (get extended weather or get limited weather) depending on if the user is signed in or not.

layout.html - the html template is quite similar to the one in Finance. The changes were made in the navigation bar, the logo is changed, position of navigation bar elements is changed, background image is changed through css styling etc.

login.html; register.html - these templates are similar to the ones in Finance. Although some stylistic changes have been made to fit in the overall style and color settings of the weather page.

search_result.html - this template gets passed a list that is generated by the search function. A loop runs through the list, displaying a link for each individual city name. When the user clicks on a certain link, weather data for that city is displayed (another template rendered).

weatherlim.html - first element of the template is the style, which defines where certain headings are displayed. After the headings with information about the city requested, a table is displayed with table headings refering to basic weather information. In the table body, in each cell responding information about weather is displayed (temperature, description etc.) Next, there is a similar table about pressure and wind information. These two tables are displayed regardless to the user being signed in or not. Next, an if statement is used to determine if the user is signed in. Only if the condition is true the forecast table gets shown. In the table, basic information is displayed (date and weekday, minimum and maximum temperature and an icon that fits the description of the weather for the particular day). All of the information gets passed from the city function in app.py which uses the lookup function to retrieve data. Below each basic forecast for the day there are links shown, named "Hourly" which are created from the forecast dictionary. When they get clicked, hourly.html gets rendered for a particular day. At the bottom, a button "Add to favorites" is displayed, which adds the currrent city to the SQL database of favorites.











