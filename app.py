import streamlit as st
import pandas as pd
import preprocessor
import medals

df = pd.read_csv('Data/athlete_events.csv')
reg_df = pd.read_csv('Data/noc_regions.csv')

df = preprocessor.loader(df, reg_df)

menu = st.sidebar.radio(
    'Select an option',
    (
        "Medal Tally",
        "Overall Analysis",
        "Country-wise Analysis",
        "Athlete-wise Analysis"
    )
)

# st.dataframe(df)

# to show medal tally
if menu == 'Medal Tally':
    medal_tally = medals.show(df)
    st.dataframe(medal_tally)
