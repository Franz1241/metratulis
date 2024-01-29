import streamlit as st
import datetime
import polars as pl
from datetime import datetime, time, timedelta
from libs import BusNetwork
from libs.utils import route_stats

routes_df = pl.read_parquet('./static/routes.parquet')
assert routes_df.filter(pl.col('name').is_duplicated()).shape[0] == 0, 'Duplicate route names found'
estaciones_df = pl.read_csv('./static/_dim_estaciones.csv')
estaciones = {}
for row in estaciones_df.to_dicts():
    estaciones[row['id']] = row['name']

estaciones_reverse = {v: k for k, v in estaciones.items()}


# dir = 'NS'
# time_now = datetime.now().time()
time_now = time(7,0)

# day_now = datetime.now().weekday()
day_now = 2


#General settings
st.set_page_config(
    page_title="Guia Metropolitano Rutas FRG ",
    page_icon="🚌",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("Metropolitano Rutas")
st.text(f"Hora actual: {datetime.now().strftime('%H:%M:%S')}")
time_now = time(7,0)
#Create a selectbox to choose the start and end route from a list of routes
inicio = st.selectbox(
    'Elige una estación de inicio',
    list(estaciones.values()),
    index=None,
    placeholder='Escoge una estación'
)

fin = st.selectbox(
    'Elige una estación de destino',
    list(estaciones.values()),
    index=None,
    placeholder='Escoge una estación'
    
)




if st.button("Calcular Buses"):
    if inicio == fin:
        st.error("The start and end route must be different")
    elif inicio == None or fin == None:
        st.error("Select a start and end route")
    else:
        inicio = estaciones_reverse[inicio]
        fin = estaciones_reverse[fin]
        if inicio > fin:
            direction = 'SN' 
        else:
            direction = 'NS'
        routes_df = routes_df.filter(
            (pl.col('schedule').list.first()<time_now)
            &(pl.col('schedule').list.last()>time_now)
            &(pl.col('days').list.contains(day_now))
            &(pl.col('direction')==direction)
            )   
        network = BusNetwork()
        rutas = {}
        for row in routes_df.to_dicts():
            network.add_route(row['name'], row['stops'])
            rutas[row['name']] = row['commercial_name']



        path, routes = network.find_shortest_path(inicio, fin)
        unique_buses, stops = route_stats(routes, path)
        st.markdown(f"Para ir de {estaciones[inicio]} hasta {estaciones[fin]} tienes que tomar {direction}:")
        unique_buses = [rutas[x] for x in unique_buses]
        for i in range(len(unique_buses)):
            if i == 0:
                st.markdown(f"Ruta {unique_buses[i]} desde {estaciones[inicio]} hasta {estaciones[stops[i]]}")
            elif i == len(unique_buses)-1:
                st.markdown(f"Ruta {unique_buses[i]} desde {estaciones[stops[i-1]]} hasta {estaciones[fin]}")
            else:
                st.markdown(f"Ruta {unique_buses[i]} desde {estaciones[stops[i-1]]} hasta {estaciones[stops[i]]}")


    
