
import heapq
from time import sleep
from pprint import pprint
class BusNetwork:
    def __init__(self):
        self.graph = {}
        self.distances = None
    def add_route(self, route_name, stations):
        for i,station in enumerate(stations[:-1]):
            aux_stations_traveled = abs(stations[i+1] - station)
            # aux_going_back = stations[i+1] - station < 0 or False
            if aux_stations_traveled == 1:
                self.__add_edge(station,stations[i+1], route_name, aux_stations_traveled)
            elif aux_stations_traveled >1 and aux_stations_traveled <= 3:
                self.__add_edge(station,stations[i+1], route_name, aux_stations_traveled/3)
            elif aux_stations_traveled > 3 and aux_stations_traveled <= 5:
                self.__add_edge(station,stations[i+1], route_name, aux_stations_traveled/4)
            elif aux_stations_traveled > 5 and aux_stations_traveled <= 10:
                self.__add_edge(station,stations[i+1], route_name, aux_stations_traveled/6)
            elif aux_stations_traveled > 10 and aux_stations_traveled <= 20:
                self.__add_edge(station,stations[i+1], route_name, aux_stations_traveled/8)
            elif aux_stations_traveled > 20 and aux_stations_traveled <= 40:
                self.__add_edge(station,stations[i+1], route_name, aux_stations_traveled/15)
            else:
                self.__add_edge(station,stations[i+1], route_name, aux_stations_traveled/30)
            # self.__add_edge(station,stations[i+1], route_name, aux_stations_traveled)
    
    def __add_edge(self, from_station, to_station, route_name, weight):
        if from_station not in self.graph:
            self.graph[from_station] = {}
        if to_station not in self.graph:
            self.graph[to_station] = {}
        if to_station not in self.graph[from_station]:
            self.graph[from_station][to_station] = []
        
        self.graph[from_station][to_station].append((route_name, weight))
        

    def find_shortest_path(self, start, end, route_change_penalty=5):
        distances = {station: float('infinity') for station in self.graph}
        distances[start] = 0
        previous_stations = {station: None for station in self.graph}
        previous_routes = {station: None for station in self.graph}
        pq = [(0, start, None)]

        while pq:
            current_distance, current_station, current_route = heapq.heappop(pq)
            if current_distance > distances[current_station]:
                continue
            for neighbor, routes in self.graph[current_station].items():
                for route, weight in routes:
                    # Apply route change penalty
                    total_weight = weight
                    if current_route and route != current_route:
                        total_weight += route_change_penalty
                    distance = current_distance + total_weight
                    if distance <= distances[neighbor]:
                        distances[neighbor] = distance
                        previous_stations[neighbor] = current_station
                        previous_routes[neighbor] = route
                        heapq.heappush(pq, (distance, neighbor, route))
            if current_station == end:
                break
        return self.construct_path(previous_stations, previous_routes, end)



    def construct_path(self, previous_stations, previous_routes, end):
        route = []
        stations = []
        current = end
        while previous_stations[current] is not None:
            route.append(previous_routes[current])
            stations.append(current)
            current = previous_stations[current]
        return stations[::-1], route[::-1]