# SpeedIcons - Formula 1 Project
### URL: [speedicons.pythonanywhere.com](https://speedicons.pythonanywhere.com/)
## Overview
As a final project for the **CS50x course**, I chose to implement a **Formula 1**  inspired web application by utilising the programming languages of Python, HTML, JavaScript, Jinja, and SQL. The application is built with the Flask framework and uses SQLAlchemy for database operations. \
The goal of this project is to provide F1 fans with a personalized experience, offering various interactive features centred around the drivers, teams, and the current season.

### Key Features
- **Personalized Home Page:** Displays recent results and general information about the user’s favourite driver.
- **Favourite Team Page:** Personalized team page which contains information regarding the user's favourite team.
- **Current Season Calendar:** A current season calendar containing all the races of the season as well as a countdown to the next race.
- **Driver Search:** Search for a driver from the current season.
- **Constructor Search:** Search for a team from the current season.
- **Driver Championship Standing:** Shows current driver championship standings.
- **Constructor Championship Standings:** Shows current constructor championship standings.
- **News:** Displays recent F1 articles, courtesy of [Autosport.com](https://www.autosport.com/)
- **Driver Comparison Tool:** Enables users to compare two drivers from any F1 season, offering a deep dive into their stats and performance.

## Description of files
### main.py
Responsible for running the Flask web application (**app.run**). This file also sets up a scheduling job for database updates.
### __ init__ .py
In the __ init __.py file, the Flask application is initialized and configured. Also, the SQLITE3 database is assigned to the application.

### models.py
Within this file, the tables of the database are defined.

### acquire_data.py
In the acquire_data.py file I created a class which contains all the relevant methods in order to acquire the information required for the correct operation of the application. This information is gathered by utilizing the [Ergast API](https://ergast.com/mrd/) and then it's stored in an SQLITE3 database. The reasons why the information is stored in a database is firstly to diminish the time required to GET data from the API and secondly the Ergast API will be deprecated at the end of the 2024 Formula 1 Season. Therefore, since I want the application to be fully functional also after the 2024 season it was best not to fully depend on the API. All database operations are done with the help of SQLALCHEMY.

### populate_db.py
In this file I defined a function in which I create an object of the class created in **acquire_data.py** and then I call the methods of that class. \
The reason why a function is defined, is because I use it in a scheduling job, which uses this function in order to update the database weekly.

### helpers.py
In this file I defined helper functions which are used throughout the other python files which are responsible for creating the routes of the application. \
These functions are used for fetching driver and team information from the database.

### auth.py
All the routes which fall under the category of authorization such as **login, logout, register and forgot password**  are defined in the auth.py file.

### views.py
In this file the routes of personalized home page, favourite team page as well as the routes for showing driver and team information that the user has search for, and the current season calendar are defined.

### search.py
The routes for searching for driver **/search/driver** and constructor **/search/constructor** and defined in this file.

### standings.py
Driver championship standings **/standings/driver** and constructor championship standings **/standings/constructor** routes are defined.

### news.py
The route **/news** for displaying F1 news is defined. Within this route the [News API](https://newsapi.org/) is utilized in order to fetch the news.

### compare.py
The routes for searching for the drivers to compare as well as for displaying the results of the comparison are defined in compare.py. \
**/compare** renders the page for comparing the drivers \
**/compare/search** handles the GET requests when the user is searching for drivers to compare \
**/compare/results** computes all the results that will be rendered for the comparison

## Templates
The templates subfolder contains all **.html files**. \
The main .html file is **base.html** which sets up the layout for each page in the web application, like the navbar, background and footer. The rest of the .html files inherit the code of base.html but also they add their own in order to fulfil the functionality of the route they are referring to.

## Static
The static subfolder contains the images that are displayed in the web app but also the css file and the JavaScript files.\
The styles.css file is responsible for the design of the html pages.\
The JavaScript files contribute to the additional functionality that some of the roots require.

### register.js
Depending on whether the favourite driver select tag is chosen, the margin of the select tag is adjusted through the js code in order to make all the select options i.e. the drivers, visible in the viewport



https://github.com/user-attachments/assets/a2cc9d98-d3ed-442c-bcda-049a17fda555



### driver.js & constructor.js
Handles the redirection to the pages for searched drivers or constructors.

### countdown.js
Powers the countdown feature in the **/calendar** route


https://github.com/user-attachments/assets/c38ed505-b790-4204-bd32-9174f5f7e5e0


### comapre.js
Adds the functionality of filtering out potential matches to the search query of the user. This is accomplished by sending a GET request to the /compare/search route in which drivers that match the query are selected from the database and returned as a response to the GET request of the js file.



https://github.com/user-attachments/assets/2bd4bc27-8588-416f-8a37-d6d43977abe1

### compare_result.js
Handles dynamic styling and displays driver comparison graphs such as drivers points throughout the seasons, win ratio and podium ratio using **plotly.js** .



https://github.com/user-attachments/assets/1dbc8a41-0afa-44ea-b021-486e0d15668a



## How to view the web application
#### 1) Visit this URL: [speedicons.pythonanywhere.com](https://speedicons.pythonanywhere.com/)
### **OR**
#### 2) Run the web app localy by executing: **python main.py**
