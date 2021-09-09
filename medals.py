import numpy as np
import pandas as pd


def show(df):
    # dropping all the columns where the medals would be same for team event
    mt = df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])

    # grouping the medals based on country
    mt = mt.groupby('Country').sum()[['Gold', 'Silver', 'Bronze']].sort_values(
        'Gold', ascending=False).reset_index()

    # creating a total column
    mt['Total'] = mt['Gold'] + mt['Silver'] + mt['Bronze']

    mt['Gold'] = mt['Gold'].astype(int)
    mt['Silver'] = mt['Silver'].astype(int)
    mt['Bronze'] = mt['Bronze'].astype(int)
    mt['Total'] = mt['Total'].astype(int)

    return mt


def country_year_list(df):
    # for years
    year = df['Year'].unique().tolist()
    year.sort()
    year.insert(0, 'Overall')

    # for countries
    country = df['Country']
    country = country.dropna().values
    country = np.unique(country).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return year, country


def get_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df

    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['Country'] == country]

    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]

    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year))
                           & (medal_df['Country'] == country)]

    if flag == 1:
        # grouping this medal tally according to year
        t = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values(
            'Year', ascending=True).reset_index()
    else:
        # grouping this medal tally according to country
        t = temp_df.groupby('Country').sum()[['Gold', 'Silver', 'Bronze']].sort_values(
            'Gold', ascending=False).reset_index()

    # getting total medals
    t['Total'] = t['Gold'] + t['Silver'] + t['Bronze']

    t['Gold'] = t['Gold'].astype(int)
    t['Silver'] = t['Silver'].astype(int)
    t['Bronze'] = t['Bronze'].astype(int)
    t['Total'] = t['Total'].astype(int)

    return t
