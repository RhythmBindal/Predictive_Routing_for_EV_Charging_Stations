# Predictive_Routing_for_EV_Charging_Stations

This repository contains a project that aims to provide a predictive routing solution for electric vehicle (EV) users, taking into account EV charging station locations, battery charge, and charging time. The project utilizes a road network graph, EV charging station data, and machine learning techniques to calculate the shortest path and recommend the nearest charging station if necessary.

## Dataset
The dataset used in this project consists of EV charging station information in Delhi, India procured from Delhi Government's official website. It includes attributes such as latitude, longitude, payment modes, vendor names, and station types. The dataset has been preprocessed to remove duplicates and encode categorical variables. The csv document consists of 25 columns across 2706 rows. 

## Installation
To download and run the model, follow these steps:


**Clone the repository:**
shell
Copy code

```git clone https://github.com/RhythmBindal/Predictive_Routing_for_EV_Charging_Stations.git```

**Change to the project directory:**
shell
Copy code

```cd Predictive_Routing_for_EV_Charging_Stations```

**Install the required dependencies:**
shell
Copy code

```pip install -r requirements.txt```

**Run the Streamlit application:**
shell
Copy code

```streamlit run app.py```

Access the application in your web browser at http://localhost:8501.

## Algorithms and Procedure
The project follows the following steps:

**1. Network Graph Generation:**

Utilizes the OSMnx library to obtain OpenStreetMap data for Delhi.
Creates a road network graph using the obtained data.
Projects the graph to Universal Transverse Mercator (UTM) for accurate distance calculations.
EV Charging Station Integration:

**2. Loads the EV charging station data from the dataset.**
Converts the charging station data into a GeoDataFrame, associating it with the network graph.
Finds the nearest graph nodes for each charging station using OSMnx's nearest_nodes function.
Adds charging stations as nodes in the graph, with attributes such as name, latitude, and longitude.
Streamlit Web Application:

**3. Develops a user interface using Streamlit for user interaction.**
Allows users to input their starting and destination addresses, battery charge, and charging time.
Calculates the shortest path using Dijkstra's algorithm, considering the battery range.
Recommends the nearest charging station if the destination is beyond the battery range.
Displays the optimal route on an interactive map and provides relevant information.

Original authors : Rhythm Bindal and Aarohi Manchanda
Feel free to open branches and drop in contributions. 
