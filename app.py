import pandas as pd
import plotly.graph_objs as go
import json
import plotly.express as px
import streamlit as st
from copy import deepcopy

st.title('Mapa de calor da população brasileira por etinia')

@st.cache
def load_data(path):
    df = pd.read_csv(path)
    return df    


# LOAD ENERGY DATA
df_raw = load_data(path="Populacao_por_etnia_raca.csv")
df = deepcopy(df_raw)


#LOAD GEIJASON FILE
with open("geojsonMunicipiosBrasil.json") as response:
    counties = json.load(response)

option = st.selectbox('Selecione uma Etinia:', ['Branca','Parda','Outro'])


with st.spinner('Carregando...'):
    if option != 'Outro':
        # Geographic Map
        fig = go.Figure(
            go.Choroplethmapbox(
                geojson = counties,
                locations = df['id'],
                z=df[option],
                colorscale="sunsetdark",
                marker_opacity=0.8,
                marker_line_width=0,
                hovertemplate= df['Município'],
            
                
            )
        )
        fig.update_layout(
            mapbox_style="white-bg",
            mapbox_zoom=3.2,
            mapbox_center = {"lat": -11.740856, "lon": -54.604602},
            width=800,
            height=650,
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            )
        
        st.plotly_chart(fig)
    else:
        #Vencedor
        fig2 = go.Figure(px.choropleth_mapbox(df, geojson=counties, locations='id', color='Vencedor',
                                color_continuous_scale="Viridis",
                                mapbox_style="carto-positron",
                                zoom=3, 
                                center = {"lat": -10.704459239815383, "lon": -50.771587751708005},
                                opacity=0.5,
                                hover_name='Município',
                                
                                ))

        fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                    width=800,
                    height=600,
                    mapbox_style="white-bg",
                    #marker_line_width=0,
                
                    )
        
        st.plotly_chart(fig2)

if st.checkbox('Show raw data'):
                    st.subheader('Raw Data')
                    st.dataframe(df)
                    st.download_button('Download raw data', 
                                        df.to_csv(), 
                                        file_name='Populacao_por_etnia_raca.csv',
                                        mime='text/csv')

