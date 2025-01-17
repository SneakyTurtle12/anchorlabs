import streamlit as st
import pandas as pd
import geopandas as gpd 
import matplotlib
import numpy as np
import json
import plotly.express as px
import streamlit_vertical_slider as svs
import matplotlib.pyplot as plt

st.set_page_config(layout='wide')
input_weighting = st.container(border=True)
output_graph = st.container(border=True)

df = pd.read_csv("Kenya_MCDA_Criteria_new.csv")
basin_id = df['Basin_ID2']
roi_score = df['ROI score']
pop_dense = df['Normalised Pop density']
pov_distribute = df['Normalized Poverty Distribution  ']
bio_diverse = df['Biodiversity normalised']
climate_vul = df['Climate_Vulnerability']



with input_weighting:
    st.header("Choose weightings for each of the criteria")
    in_left_col, in_right_col = st.columns(2)
    with in_left_col:
        sliders = st.container(border=True)
        with sliders:
            s_1, s_2, s_3, s_4, s_5 = st.columns(5)
            with s_1:
                roi_weight = svs.vertical_slider(label="ROI weight", default_value=0, min_value=0, max_value=100, track_color="#00AAFF", slider_color="#00FFAA", thumb_color="#00FFAA", value_always_visible=True)
            with s_2:
                pop_dense_weight = svs.vertical_slider(label="Population density weight", default_value=0, min_value=0, max_value=100, track_color="#00AAFF", slider_color="#00FFAA", thumb_color="#00FFAA", value_always_visible=True)
            with s_3:
                pov_distribute_weight = svs.vertical_slider(label="Poverty distribution weight", default_value=0, min_value=0, max_value=100, track_color="#00AAFF", slider_color="#00FFAA", thumb_color="#00FFAA", value_always_visible=True)
            with s_4:
                bio_diverse_weight = svs.vertical_slider(label="Bio-diversity weight", default_value=0, min_value=0, max_value=100, track_color="#00AAFF", slider_color="#00FFAA", thumb_color="#00FFAA", value_always_visible=True)
            with s_5:
                climate_vul_weight = svs.vertical_slider(label="Climate vulnerability weight", default_value=0, min_value= 0, max_value=100, track_color="#00AAFF", slider_color="#00FFAA", thumb_color="#00FFAA", value_always_visible=True)
            st.write(str(roi_weight)+ ' ' + str(pop_dense_weight))
            weighted_score = roi_score*roi_weight + pop_dense*pop_dense_weight + pov_distribute*pov_distribute_weight + bio_diverse*bio_diverse_weight + climate_vul*climate_vul_weight
            max_score = max(weighted_score)
            weighted_score = (weighted_score/max_score)*100
            
    weighted_df = pd.DataFrame(
        {'Basin_ID2': basin_id,
          'Overall_score': weighted_score}
        )
    weighted_df.columns = ['Basin_ID2', 'Overall_score']


    with in_right_col:
            pie_contain= st.container(border=True)
            with pie_contain:
                aspects_weighted_data = [['ROI', roi_weight],['Population density', pop_dense_weight],['Poverty Distribution', pov_distribute_weight],['Bio-diversity', bio_diverse_weight],['Climate vulnerability', climate_vul_weight]]
                aspects_weighted_df = pd.DataFrame(aspects_weighted_data)
                aspects_weighted_df.columns = ['Aspect', 'Weighting']
                pie_c = px.pie(aspects_weighted_df, values='Weighting', names='Aspect', title='Your chosen weightings of each aspect')
                st.plotly_chart(pie_c, theme='streamlit', use_container_width=True)




#123skylar was here

with output_graph:
    out_left_col, out_right_col = st.columns(2)
    with out_left_col:
        #weighted_df = pd.read_csv('Basin_value.csv')
        shapefile= gpd.read_file('WRA_SubBasins_v2_added_variables.shp')
        shapefile = shapefile.merge(weighted_df, on='Basin_ID2')
        fig, ax = plt.subplots(1, figsize=(10, 6))
        ax.axis('off')
        ax.set_facecolor("red")
        ax.set_title('waterbasin investments in kenya', fontdict={'fontsize': '15', 'fontweight' : '3'})
        shapefile.plot(column='Overall_score',
                    cmap='inferno_r',
                    linewidth=0.2,
                    ax=ax,
                    edgecolor='1',
                    legend=True, missing_kwds={
                    "color": "lightgrey",
                    "label": "Missing values",},)
        fig.savefig('look_at_this_graph.jpg',bbox_inches='tight', dpi=300)

        st.pyplot(fig)
