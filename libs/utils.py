def route_stats(routes, path):
    unique_buses= []
    stops = []
    aux_current = None
    for x,y in enumerate(routes):
        if y != aux_current:
            unique_buses.append(y)
            if x != 0:
                stops.append(path[x-1])
            aux_current = y
    stops.append(path[-1])
    return unique_buses, stops