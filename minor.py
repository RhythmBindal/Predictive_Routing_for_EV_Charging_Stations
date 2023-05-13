import streamlit as st
import osmnx as ox
import networkx as nx
import pandas as pd

# Load the graph (assuming you have saved it as 'delhi_ev_graph.graphml')
G = ox.load_graphml('delhi_ev_graph.graphml')

# Define a function to compute the battery range gained by charging for a specified time
def compute_battery_range(charging_time):
    # Compute the battery range gained by charging for the specified time
    battery_range_gained = charging_time * 60  # Assume 60 km of range gained per hour of charging
    
    return battery_range_gained

# Streamlit app layout
st.title("EV Routing Application")

start_address = st.text_input("Enter starting address:", value="")
end_address = st.text_input("Enter destination address:", value="")
battery_charge = st.number_input("Enter current battery charge (in kilometers):", value=0)
charging_time = st.number_input("Enter charging time (in hours):", value=0)

if start_address and end_address and battery_charge is not None and charging_time is not None:
    # Geocode the addresses to get coordinates
    start_location = ox.geocode(start_address)
    end_location = ox.geocode(end_address) 

    # Find the nearest nodes to the starting and ending points
    start_node = ox.distance.nearest_nodes(G, X=[start_location[1]], Y=[start_location[0]], return_dist=False)[0]
    end_node = ox.distance.nearest_nodes(G, X=[end_location[1]], Y=[end_location[0]], return_dist=False)[0]

    # Compute the battery range gained by charging for the specified time
    battery_range_gained = compute_battery_range(charging_time)

    # Compute the battery range considering the current battery charge and charging time
    battery_range = battery_charge + battery_range_gained

    # Compute the shortest path using Dijkstra's algorithm based on distance and battery constraints
    shortest_path = shortest_path_with_constraints(G, start_node, end_node, battery_range, charging_time, weight='length')
    shortest_path_distance = nx.shortest_path_length(G, source=start_node, target=end_node, weight='length')

    # Display the route information
    st.write(f"Shortest path: {shortest_path}")
    st.write(f"Total distance: {shortest_path_distance:.2f} km")

    # Visualize the route on a map
    fig, ax = ox.plot_graph_route(G, shortest_path, route_linewidth=6, node_size=0, bgcolor='k', edge_color='w', edge_linewidth=0.5, show=False, close=False)
    
    # Check if the battery charge is sufficient to reach the destination
    if shortest_path_distance > battery_range:
        # Find the nearest charging station to the destination
        nearest_charging_station = find_nearest_charging_station(G, end_node)
        st.write(f"Battery charge insufficient to reach the destination. Nearest charging station: {nearest_charging_station}")
