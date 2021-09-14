def year_wise_medal_tally(df, country):
    cm = df.dropna(subset=['Medal'])
    cm = cm.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    cm = cm[cm['Country'] == country]
    cm = cm.groupby('Year').count()['Medal'].reset_index()
    return cm


def country_event_heatmap(df, country):
    best_sport = cm = df.dropna(subset=['Medal'])
    best_sport = best_sport.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    best_sport = best_sport[best_sport['Country'] == country]

    # making a pivot table
    pt = best_sport.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count')
    pt = pt.fillna(0).astype('int')
    return pt


def successful_athlete(df, country):
    temp = df.dropna(subset=['Medal'])
    temp = temp[temp['Country'] == country]
    temp = temp['Name'].value_counts().reset_index()
    temp = temp.merge(df, left_on='index', right_on='Name', how='left')
    temp = temp[['index', 'Name_x', 'Sport']]
    temp = temp.drop_duplicates('index')
    temp.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return temp.head(10)
