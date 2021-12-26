import streamlit as st
import pandas as pd
import numpy as np
from zipfile import ZipFile
import plotly.express as px

st.title("Glow Baby Data")

file = st.file_uploader('Upload gzip export')

if file:
    with ZipFile(file) as myzip:
        
        # get file names
        sub_files = myzip.namelist()
        daiper_file = next((s for s in sub_files if 'Diaper' in s), None)
        breast_feed_file = next((s for s in sub_files if 'Breast' in s), None)
        sleep_file = next((s for s in sub_files if 'Sleep' in s), None)


        # nappies
        st.subheader('Nappy Changing...')
        with myzip.open(daiper_file) as myfile:          
            
            
            df = pd.read_csv(
                myfile,
            )
            df['Diaper time'] = pd.to_datetime(df['Diaper time'])

            # plot nappies per day
            df['day'] = df['Diaper time'].dt.round('D')
            dfg = df.groupby('day').count()
            fig = px.bar(
                dfg[['Diaper time']],
                labels={'day': 'Date', 'value':'Count'},
                title='Changes Per Day',
            )
            fig.update_layout(showlegend=False)
            fig.update_traces(marker=dict(color="orange"))
            st.plotly_chart(fig)
            
            # plot nappy hours
            df['hour'] = df['Diaper time'].dt.hour
            dfg = df.groupby('hour').count()
            fig = px.bar(
                dfg[['Diaper time']],
                labels={'hour': 'Hour', 'value':'Count'},
                title='Changes Per Hour',
            )
            fig.update_layout(showlegend=False)
            fig.update_traces(marker=dict(color="orange"))
            st.plotly_chart(fig)


        # feeds
        st.subheader('Breast Feeding...')
        with myzip.open(breast_feed_file) as myfile:
            df = pd.read_csv(
                myfile,
            )
            df['Begin time'] = pd.to_datetime(df['Begin time'])
            df['both'] = df['Left(min)'] + df['Right(min)']

            # plot feeds per day
            df['day'] = df['Begin time'].dt.round('D')
            dfg = df.groupby('day').count()
            fig = px.bar(
                dfg[['both']],
                labels={'day': 'Date', 'value':'Count'},
                title='Feeds Per Day',
            )
            fig.update_layout(showlegend=False)
            fig.update_traces(marker=dict(color="orange"))
            st.plotly_chart(fig)

            # plot total minutes per day
            dfg = df.groupby('day').sum()
            fig = px.bar(
                dfg[['both']],
                labels={'day': 'Date', 'value':'Time (mins)'},
                title='Total Time Per Day',
            )
            fig.update_layout(showlegend=False)
            fig.update_traces(marker=dict(color="orange"))
            st.plotly_chart(fig)

            # plot feeds per hour
            df['hour'] = df['Begin time'].dt.hour
            dfg = df.groupby('hour').count()
            fig = px.bar(
                dfg[['both']],
                labels={'hour': 'Hour', 'value':'Count'},
                title='Feeds Per Hour',
            )
            fig.update_layout(showlegend=False)
            fig.update_traces(marker=dict(color="orange"))
            st.plotly_chart(fig)


