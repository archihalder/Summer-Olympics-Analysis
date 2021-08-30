def show(df):
    # dropping all the columns where the medals would be same for team event
    mt = df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])

    # grouping the medals based on region
    mt = mt.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values(
        'Gold', ascending=False).reset_index()

    # creating a total column
    mt['Total'] = mt['Gold'] + mt['Silver'] + mt['Bronze']

    mt['Gold'] = mt['Gold'].astype(int)
    mt['Silver'] = mt['Silver'].astype(int)
    mt['Bronze'] = mt['Bronze'].astype(int)
    mt['Total'] = mt['Total'].astype(int)

    return mt
