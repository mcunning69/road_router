#! python3

"""ROAD ROUTER
Route from servers along all roads using the Dijkstra routing algorithm
while finding the nearest server to each road segment
(called from main.py)."""

import data_input_output as dio
import dijkstar  # pip install dijkstar (https://pypi.org/project/Dijkstar/)
import math
import numpy as np

MAX_SEPARATION = 1  # for close points to be considered junctions (in metres)


def cost_func(u, v, e, prev_e):
    """Cost function for the Dijkstra routing algorithm."""
    return e['cost']


def route(snode, rnode, rpoint, rseg):
    """Route servers to roads using the Dijkstra routing algorithm."""

    # Calculate road segment lengths
    for i, item in enumerate(rseg):
        rseg[i]['length'] = math.hypot(
            item['x2'] - item['x1'], item['y2'] - item['y1'])

    # Find nearest single road point to link each server node
    # (note: 2nd/3rd server-road links might be needed but not modelled here)
    for i in range(len(snode)):
        sldist = [math.hypot(jtem['x'] - snode[i]['x'],
                             jtem['y'] - snode[i]['y']) for jtem in rpoint]
        mindist = min(sldist)
        if mindist < snode[i]['nearest_pt_sl_dist']:
            snode[i]['nearest_pt'] = np.argmin(sldist)
            snode[i]['nearest_pt_sl_dist'] = mindist

    # Add "edges" for road segments while avoiding duplicates
    edge = []
    found_edge = []
    for item in rseg:
        cur_edge = {
            'u': item['point1'],
            'v': item['point2'],
            'length': item['length']}
        if (cur_edge['u'], cur_edge['v']) not in found_edge:
            edge.append(cur_edge)
            found_edge.append((cur_edge['u'], cur_edge['v']))

    # Find road junctions and add them as edges while avoiding duplicates
    for i in range(len(rpoint)):
        for j in range(len(rpoint)):
            if (j != i) and (
                math.hypot(rpoint[j]['x'] - rpoint[i]['x'],
                           rpoint[j]['y'] - rpoint[i]['y']) < MAX_SEPARATION):
                cur_edge = {'u': min(j, i), 'v': max(j, i), 'length': 0}
                if cur_edge not in found_edge:
                    edge.append(cur_edge)
                    found_edge.append((cur_edge['u'], cur_edge['v']))

    # Build the routing "graph" for the Dijkstra algorithm
    graph = dijkstar.Graph()
    for item in edge:
        graph.add_edge(item['u'], item['v'], {'cost': item['length']})
        graph.add_edge(item['v'], item['u'], {'cost': item['length']})

    # Route each each server node to all reachable road points
    dpaths = dijkstar.algorithm.single_source_shortest_paths
    dextract = dijkstar.algorithm.extract_shortest_path_from_predecessor_list
    for i in range(len(snode)):
        try:
            predecessors = dpaths(
                graph, snode[i]['nearest_pt'], cost_func=cost_func)
        except dijkstar.algorithm.NoPathError:
            predecessors = None

        # Extract the shortest path for each road point on the path tree
        if predecessors is not None:
            for jtem in predecessors:
                path = dextract(predecessors, jtem)

                # Set the road point to colour of its best server node so far
                if (path is not None) and (
                        path.total_cost < rpoint[jtem]['lowest_cost']):
                    rpoint[jtem]['lowest_cost'] = path.total_cost
                    rpoint[jtem]['best_server'] = i
                    rpoint[jtem]['color_num'] = snode[i]['color_num']

    # Set road segments to the colour of their best servers
    for i, item in enumerate(rseg):
        point1_bs = rpoint[item['point1']]['best_server']
        point2_bs = rpoint[item['point2']]['best_server']
        if (point1_bs is None) and (point2_bs is None):
            rseg[i]['best_server'] = None
        elif (point1_bs is None):
            rseg[i]['best_server'] = point2_bs
        elif (point2_bs is None):
            rseg[i]['best_server'] = point1_bs
        else:
            # Determine which road segment endpoint is nearest to a server
            point1_sl_dist = math.hypot(
                item['x1'] - snode[point1_bs]['x'],
                item['y1'] - snode[point1_bs]['y'])
            point2_sl_dist = math.hypot(
                item['x2'] - snode[point2_bs]['x'],
                item['y2'] - snode[point2_bs]['y'])
            if point1_sl_dist <= point2_sl_dist:
                rseg[i]['best_server'] = point1_bs
            else:
                rseg[i]['best_server'] = point2_bs
        if rseg[i]['best_server'] is not None:
            rseg[i]['color_num'] = snode[rseg[i]['best_server']]['color_num']

    # Set road nodes to the colour of their best servers
    for i in range(len(rnode)):
        for jtem in rpoint:
            if math.hypot(jtem['x'] - rnode[i]['x'],
                          jtem['y'] - rnode[i]['y']) < MAX_SEPARATION:
                rnode[i]['best_server'] = jtem['best_server']
                rnode[i]['color_num'] = jtem['color_num']

    return snode, rnode, rpoint, rseg
