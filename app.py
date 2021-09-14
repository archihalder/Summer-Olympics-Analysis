import streamlit as st
import pandas as pd
import preprocessor
import medals
import overall_analysis as oa
import country_wise_analysis as cwa
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

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

if menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nation = df['Country'].unique().shape[0]

    st.title('Top Statistics')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Cities')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col4, col5, col6 = st.columns(3)
    with col4:
        st.header('Events')
        st.title(events)
    with col5:
        st.header('Athletes')
        st.title(athletes)
    with col6:
        st.header('Countries')
        st.title(nation)

    nations_over_time = oa.data_over_time(df, 'Country')
    fig = px.line(nations_over_time, x='Year', y='Country')
    st.title('Participating Nations over the years')
    st.plotly_chart(fig)

    events_over_time = oa.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x='Year', y='Event')
    st.title('Events over the years')
    st.plotly_chart(fig)

    athletes_over_time = oa.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x='Year', y='Name')
    st.title('Number of athletes participated over the years')
    st.plotly_chart(fig)

    st.title('Number of Events played over time (All Sports)')
    fig, ax = plt.subplots(figsize=(20, 20))
    pt = df.drop_duplicates(['Year', 'Sport', 'Event'])
    pt = pt.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int')
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    # Creating list of sports played
    sp = df['Sport'].unique().tolist()
    sp.sort()
    sp.insert(0, 'Overall')

    st.title('Most Successful Athletes in Olympic History')
    selected_sport = st.selectbox('Select Sport', sp)
    msa = oa.most_successful(df, selected_sport)
    st.table(msa)

if menu == 'Country-wise Analysis':

    # country list
    country_list = df['Country'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select the Country', country_list)

    # year-wise medal tally
    country_df = cwa.year_wise_medal_tally(df, selected_country)
    st.title('Year-wise Medal Tally of ' + selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.plotly_chart(fig)

    # most successful athletes
    st.title('Most successful athletes of ' + selected_country)
    best_athlete = cwa.successful_athlete(df, selected_country)
    st.table(best_athlete)

    # event-wise heatmap
    st.title('Event-wise Performance of ' + selected_country)
    heat_map = cwa.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(heat_map, annot=True)
    st.pyplot(fig)
