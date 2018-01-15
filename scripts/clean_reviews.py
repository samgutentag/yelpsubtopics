import numpy as np
import pandas as pd
import datetime
import json

DRY_RUN = False

day_labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def time_marker(text=''):
    print('[{}] {}'.format(datetime.datetime.now().time(), text.title()))

def unpack(df, column, fillna=None):
    ret = None
    if fillna is None:
        ret = pd.concat([df, pd.DataFrame((d for idx, d in df[column].iteritems()))], axis=1)
        del ret[column]
    else:
        ret = pd.concat([df, pd.DataFrame((d for idx, d in df[column].iteritems())).fillna(fillna)], axis=1)
        del ret[column]
    return ret


#-------------------------------------------------------------------------------
time_marker(text='Loading Reviews Data...')

data = pd.DataFrame()
source_data_file = '../source_data/review.json'

reviews_list = []
for line in open(source_data_file, 'r'):
    reviews_list.append(json.loads(line))

time_marker(text='creating dataframe...')
reviews_df = pd.DataFrame(reviews_list)

time_marker(text='correcting data type...')
reviews_df.date        = pd.to_datetime(reviews_df.date)


#-------------------------------------------------------------------------------
time_marker(text='sanitizing review text for csv...')
reviews_df['text'] = reviews_df['text'].str.strip()
reviews_df['text'] = reviews_df['text'].str.replace(',', ' ')



#-------------------------------------------------------------------------------
time_marker(text='Writing to files...')

for year in reviews_df.date.dt.year.unique()):
    df = reviews_df[reviews_df.date.dt.year == year].copy()
    df.reset_index(inplace=True, drop=True)

    file_name = '../clean_data/reviews/{:d}_reviews_clean.csv'.format(year)
    time_marker(text='Writing {:d} records file...'.format(year))
    if DRY_RUN:
        pass
    else:
        df.to_csv(file_name, encoding='utf-8')


#-------------------------------------------------------------------------------
time_marker(text='Complete!')
