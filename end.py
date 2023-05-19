import streamlit as st
import osmnx as ox
import networkx as nx
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from geopy.distance import great_circle

# Load the graph
G = ox.load_graphml('delhi_ev_graph.graphml')

import pandas as pd

# Load the processed DataFrame
df = pd.read_csv("processed_ev_data.csv")

# Get the nodes with charging stations
charging_station_nodes = [node for node, data in G.nodes(data=True) if data.get('charging_station', False)]

def find_nearest_charging_station(G, current_node, charging_station_nodes):
    min_distance = float("inf")
    nearest_charging_station = None
    payment_mode = None
    for charging_station in charging_station_nodes:
        distance = nx.shortest_path_length(G, current_node, charging_station, weight='length')
        if distance < min_distance:
            min_distance = distance
            nearest_charging_station = charging_station
            payment_mode = payment_modes[charging_station]
    return nearest_charging_station, payment_mode
    for charging_station in charging_station_nodes:
        distance = nx.shortest_path_length(G, current_node, charging_station, weight='length')
        if distance < min_distance:
            min_distance = distance
            nearest_charging_station = charging_station
    return nearest_charging_station
# Create a dictionary to store the payment modes for each charging station
payment_modes = {}
for idx, row in df.iterrows():
    node_id = charging_station_nodes[idx]
    payment_mode = row['payment_modes']  # Replace 'payment_mode' with the appropriate column name in your DataFrame
    payment_modes[node_id] = payment_mode

st.title("Delhi EV Charging Stations Route Planner")

# Input fields
start_address = st.text_input("Starting address:")
end_address = st.text_input("Destination address:")
battery_range = st.number_input("Battery charge in km:", min_value=0, value=100, step=1)
charging_time = st.number_input("Charging time in minutes:", min_value=0, value=30, step=1)

if st.button("Find route"):
    if start_address and end_address:
        start_point = ox.geocode(start_address)
        end_point = ox.geocode(end_address)

        # Find nearest graph nodes
        start_node = ox.nearest_nodes(G, start_point[1], start_point[0])
        end_node = ox.nearest_nodes(G, end_point[1], end_point[0])

        # Check if the destination is within battery range
        route = nx.shortest_path(G, start_node, end_node, weight='length')
        route_length = nx.shortest_path_length(G, start_node, end_node, weight='length') / 1000

        if route_length <= battery_range:
            st.success("The destination is within your battery range. No need to stop at a charging station.")
            fig, ax = ox.plot_graph_route(G, route, route_linewidth=6, node_size=0, bgcolor='k', edge_color="w", edge_linewidth=0.5, show=False, close=False)
            st.pyplot(fig)
        else:
        nearest_charging_station = find_nearest_charging_station(G, start_node, charging_station_nodes)
        st.warning("The destination is beyond your battery range. You should stop at a charging station.")
        st.write(f"Nearest charging station: {payment_modes}".format(G.nodes[nearest_charging_station]['name']))
        
#         nearest_charging_station = find_nearest_charging_station(G, start_node, charging_station_nodes)
#         st.warning("The destination is beyond your battery range. You should stop at a charging station.")
#         st.write("Nearest charging station: {}".format(G.nodes[nearest_charging_station]['name']))
#         st.write("Payment mode: UPI")


            # Plot the route to the nearest charging station
        route_to_charging_station = nx.shortest_path(G, start_node, nearest_charging_station, weight='length')
        fig, ax = ox.plot_graph_route(G, route_to_charging_station, route_linewidth=6, node_size=0, bgcolor='k', edge_color="w", edge_linewidth=0.5, show=False, close=False)
        st.pyplot(fig)
    else:
        st.error("Please enter both starting and destination addresses.")
