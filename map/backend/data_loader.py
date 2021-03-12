import pandas as pd


def cs_info():
    df_cs_info = pd.read_csv('map/backend/data/cs_info.csv', index_col=0, header=None,
                             names=['name', 'longitude', 'latitude', 'online', 'capacity'])

    fake_cs = ['F12', 'F13', 'F15', 'S1', 'S2', 'LJDL', 'E04', 'BN0002', 'F11']
    df_cs_info = df_cs_info.loc[~df_cs_info['name'].isin(fake_cs)]
    return df_cs_info.to_dict(orient='records')
