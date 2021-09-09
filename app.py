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
    st.sidebar.header('Medal Tally')
    years, country = medals.country_year_list(df)

    selected_year = st.sidebar.selectbox('Select Year', years)
    selected_country = st.sidebar.selectbox('Select Country', country)

    medal_tally = medals.get_medal_tally(df, selected_year, selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')

    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title("Overall Performance of " + selected_country)

    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal Tally in ' + str(selected_year))

    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + "'s Performance in " + str(selected_year))

    st.table(medal_tally)
