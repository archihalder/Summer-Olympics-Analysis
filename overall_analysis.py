def participating_nations_over_time(df):
    nations_over_time = df.drop_duplicates(['Year', 'Country'])
    nations_over_time = nations_over_time['Year'].value_counts()
    nations_over_time = nations_over_time.reset_index()
    nations_over_time = nations_over_time.sort_values('index')
    nations_over_time.rename(columns={'index': 'Year', 'Year': 'No. of Countries'}, inplace=True)
    return nations_over_time
