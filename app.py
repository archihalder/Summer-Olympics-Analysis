import streamlit as st
import pandas as pd
import preprocessor
import medals
import overall_analysis as oa
import country_wise_analysis as cwa
import athlete_wise_analysis as awa
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('Data/athlete_events.csv')
reg_df = pd.read_csv('Data/noc_regions.csv')

df = preprocessor.loader(df, reg_df)

st.sidebar.title('Summer Olympics Analysis')
st.sidebar.image('Data/logo.png')
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

if menu == 'Athlete-wise Analysis':

    # Distribution of Age wrt Medals
    athlete_df = df.drop_duplicates(subset=['Name', 'Country'])
    age_df = athlete_df['Age'].dropna()
    gold_df = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    silver_df = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    bronze_df = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    dist = ff.create_distplot(
        [age_df, gold_df, silver_df, bronze_df],
        ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
        show_hist=False, show_rug=False)
    dist.update_layout(autosize=False, width=800, height=600)
    st.title('Distribution of Age w.r.t Medals')
    st.plotly_chart(dist)

    # Distribution of Age wrt Sports (only Gold Medals)
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    x = []
    sport_name = []
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        sport_name.append(sport)

    fig = ff.create_distplot(x, sport_name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=800, height=600)
    st.title("Distribution of Age w.r.t Sports (Gold Medalist)")
    st.plotly_chart(fig)

    # Scatterplot of Height and Weight of athletes
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = awa.height_and_weight(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(temp_df['Weight'], temp_df['Height'],
                         hue=temp_df['Medal'], style=temp_df['Sex'], s=20)
    fig.set_size_inches(12, 8)
    st.pyplot(fig)

    st.title('Men vs Women Participation over the years')
    both = awa.men_vs_women(df)
    fig = px.line(both, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=800, height=600)
    st.plotly_chart(fig)
