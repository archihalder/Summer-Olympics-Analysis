def data_over_time(df, col):
    data = df.drop_duplicates(['Year', col])
    data = data['Year'].value_counts()
    data = data.reset_index()
    data = data.sort_values('index')
    data.rename(columns={'index': 'Year', 'Year': col}, inplace=True)
    return data


def most_successful(df, sport):
    temp = df.dropna(subset=['Medal'])
    if sport != 'Overall':
        temp = temp[temp['Sport'] == sport]
    temp = temp['Name'].value_counts()
    temp = temp.reset_index()
    temp = temp.merge(df, left_on='index', right_on='Name', how='left')
    temp = temp[['index', 'Name_x', 'Sport', 'Country']]
    temp = temp.drop_duplicates('index')
    temp.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return temp.head(10)
