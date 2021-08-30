import pandas as pd


def loader(df, region_df):
    # filtering based on Summer Season
    df = df[df['Season'] == 'Summer']

    # merging df with region_df based on NOC
    df = df.merge(region_df, on='NOC', how='left')

    # removing the duplicates
    df.drop_duplicates(inplace=True)

    # one-hot encoding Medals and concatenating with df
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)

    return df
