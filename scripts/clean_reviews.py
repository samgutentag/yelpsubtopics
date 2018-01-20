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
time_marker('appending bid_prefix column...')
reviews_df['bid_prefix'] = reviews_df.business_id.apply(lambda x: x[:1])

#-------------------------------------------------------------------------------
time_marker(text='Writing to files...')
file_count = len(reviews_df.bid_prefix.unique())

import string
translator = str.maketrans('','', string.punctuation)

for i, prefix in enumerate(sorted(reviews_df.bid_prefix.unique())):

    # take subset of busineses and trim business_id_refix column
    df = reviews_df[reviews_df.bid_prefix == prefix].iloc[:,:-1].copy()


    # drop reviews with missing review text
    time_marker('\tdrop reviews with missing review text...')
    df = df[~df.text.isnull()].copy()

    # lowercase text and remove puncutation
    time_marker('\tlowercase text and remove puncutation...')
    df['text'] = df['text'].apply(lambda text: text.translate(translator).lower())

    # append text length columns
    time_marker('\tappend text length columns ...')
    df['review_length'] = df.text.str.len()

    df.reset_index(inplace=True, drop=True)
    file_name = '../clean_data/reviews/{}_{}_reviews_clean.csv'.format(str(i).zfill(2), prefix)
    time_marker(text='Writing {:d} records to file {}'.format(df.shape[0], file_name))
    if DRY_RUN:
        pass
    else:
        df.to_csv(file_name, encoding='utf-8')
time_marker(text='Done!')




#-------------------------------------------------------------------------------
time_marker(text='Complete!')
