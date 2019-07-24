#! python3

"""ROAD ROUTER
Main program
Version 1.00."""

import data_input_output as dio
import router as rt

# Load CSV file data from QGIS
server_node, road_node, road_segment_point = dio.load_data()

# Extract working data from CSV import
snode, rnode, rpoint, rseg = dio.setup_nodes(
    server_node, road_node, road_segment_point)

# Route servers to nearest road segments and nodes
snode, rnode, rpoint, rseg = rt.route(snode, rnode, rpoint, rseg)

# Plot results and save to PDF file
dio.plot_nodes(snode, rnode, rseg)

# Export results to CSV for import to QGIS
road_node, road_segment_point = dio.prep_export(
    road_node, road_segment_point,
    snode, rnode, rpoint)
dio.save_data(road_node, road_segment_point)
