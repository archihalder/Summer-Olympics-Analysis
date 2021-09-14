def height_and_weight(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'Country'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df


def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'Country'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    both = men.merge(women, on='Year', how='left')
    both.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    both.fillna(0, inplace=True)
    return both
