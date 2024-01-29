import polars as pl
pl.Config().set_tbl_rows(1000)
pl.Config().set_fmt_str_lengths(50)
pl.Config().set_fmt_table_cell_list_len(20)
from datetime import datetime, time, timedelta

import sys

sys.path.append('../')

from libs import BusNetwork

def route_stats(routes, path):
    unique_buses= []
    stops = []
    aux_current = None
    for x,y in enumerate(routes):
        if y != aux_current:
            unique_buses.append(y)
            if x != 0:
                stops.append(path[x-1])
                # stops.append(path[x])

            aux_current = y
    stops.append(path[-1])
    return unique_buses, stops


routes_df = pl.read_parquet('../static/routes.parquet')
assert routes_df.filter(pl.col('name').is_duplicated()).shape[0] == 0, 'Duplicate route names found'
estaciones_df = pl.read_csv('../static/_dim_estaciones.csv')
estaciones = {}
for row in estaciones_df.to_dicts():
    estaciones[row['id']] = row['name']


dir = 'NS'
# time_now = datetime.now().time()
time_now = time(7,0)
# day_now = datetime.now().weekday()
day_now = 2



inicio = 10
fin = 34
# inicio = 1
# fin = 7

routes_df = routes_df.filter(
    (pl.col('schedule').list.first()<time_now)
    &(pl.col('schedule').list.last()>time_now)
    &(pl.col('days').list.contains(day_now))
    &(pl.col('direction')==dir)
    # &(pl.col('stops').list.min()>=inicio)
    # &(pl.col('stops').list.max()<=fin)
    )
assert routes_df.shape[0] > 0, 'No routes found'
network = BusNetwork()
rutas = {}

for row in routes_df.to_dicts():

    network.add_route(row['name'], row['stops'])
    rutas[row['name']] = row['commercial_name']



path, routes = network.find_shortest_path(inicio, fin)
unique_buses, stops = route_stats(routes, path)

print(f"Para ir de {estaciones[inicio]} hasta {estaciones[fin]} tienes que tomar:")


for i in range(len(unique_buses)):
    if i == 0:
        print(f"La ruta {rutas[unique_buses[i]]} desde {estaciones[inicio]} hasta {estaciones[stops[i]]}")
    elif i == len(unique_buses)-1:
        print(f"La ruta {rutas[unique_buses[i]]} desde {estaciones[stops[i-1]]} hasta {estaciones[fin]}")
    else:
        print(f"La ruta {rutas[unique_buses[i]]} desde {estaciones[stops[i-1]]} hasta {estaciones[stops[i]]}")