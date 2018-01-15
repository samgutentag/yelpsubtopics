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
time_marker(text='Loading Business Info Data...')

data = pd.DataFrame()
source_data_file = '../source_data/business.json'

biz_list = []
for line in open(source_data_file, 'r'):
    biz_list.append(json.loads(line))

time_marker(text='creting dataframe...')
biz_df = pd.DataFrame(biz_list)

#-------------------------------------------------------------------------------
time_marker(text='collecting business Hours...')
biz_hours = biz_df[['business_id', 'hours']].copy()
biz_hours = pd.concat([biz_hours.drop(['hours'], axis=1), biz_hours['hours'].apply(pd.Series)], axis=1)


#-------------------------------------------------------------------------------
time_marker(text='Split hours into open and close...')
# split daily hours columnsinto '{DAY}_open' and '{DAY}_close'
for col in biz_hours.columns[1:]:

    # split hours column of [11:00-19:00] into '{original_name}_open' and '{original_name}_close' columns
    biz_hours['{}_open'.format(col.lower())], biz_hours['{}_close'.format(col.lower())] = biz_hours[col].str.split('-', 1).str

    # split each open column into '{}_open_hour' and '{}_open_minute' columns
    biz_hours['{}_open_hour'.format(col.lower())], biz_hours['{}_open_minute'.format(col.lower())] = biz_hours['{}_open'.format(col.lower())].str.split(':',1).str

    # split each close column into '{}_open_hour' and '{}_open_minute' columns
    biz_hours['{}_close_hour'.format(col.lower())], biz_hours['{}_close_minute'.format(col.lower())] = biz_hours['{}_close'.format(col.lower())].str.split(':',1).str

    # convert open_hour and open_minute to int, min/60 for fraction of hour
    biz_hours['{}_open_hour'.format(col.lower())] = biz_hours['{}_open_hour'.format(col.lower())].astype('float')
    biz_hours['{}_open_minute'.format(col.lower())] = biz_hours['{}_open_minute'.format(col.lower())].astype('float')/60.

    # convert close_hour and close_minute to int, min/60 for fraction of hour
    biz_hours['{}_close_hour'.format(col.lower())] = biz_hours['{}_close_hour'.format(col.lower())].astype('float')
    biz_hours['{}_close_minute'.format(col.lower())] = biz_hours['{}_close_minute'.format(col.lower())].astype('float')/60.

    # add back into hour of day as a fraction of hours in 24 hour clock i.e. 5:30pm -> 17.5
    biz_hours['{}_open'.format(col.lower())] = biz_hours['{}_open_hour'.format(col.lower())] + biz_hours['{}_open_minute'.format(col.lower())]
    biz_hours['{}_close'.format(col.lower())] = biz_hours['{}_close_hour'.format(col.lower())] + biz_hours['{}_close_minute'.format(col.lower())]

    # drop our bits and pieces
    drop_cols = ['{}_open_hour'.format(col.lower()),
         '{}_open_minute'.format(col.lower()),
         '{}_close_hour'.format(col.lower()),
         '{}_close_minute'.format(col.lower())]
    biz_hours.drop(drop_cols, axis=1, inplace=True)

    # drop oroginal column
    biz_hours.drop([col], inplace=True, axis=1)
biz_hours.fillna(0, inplace=True)

#-------------------------------------------------------------------------------
# merge back to original data frame
time_marker(text='merge open and close hours to business data...')
biz_df = biz_df.merge(biz_hours, left_on='business_id', right_on='business_id')

# drop original 'hours' column of lists
biz_df.drop(['hours'], axis=1, inplace=True)


#-------------------------------------------------------------------------------
time_marker(text='unpacking business attributes...')
biz_df = unpack(biz_df, 'attributes')


#-------------------------------------------------------------------------------
time_marker(text='cleaning up and reset index...')
biz_df.columns = [str(x).lower() for x in biz_df.columns]
biz_df.reset_index(inplace=True, drop=True)


#-------------------------------------------------------------------------------
time_marker(text='Writing to files...')

for rating in biz_df.stars.unique():
    df = biz_df[biz_df.stars == rating].copy()
    df.reset_index(inplace=True, drop=True)

    file_name = '../clean_data/business/{}_star_business_clean.csv'.format(rating.replace('.',''))
    time_marker(text='Writing {} rated records file...'.format(rating))
    if DRY_RUN:
        pass
    else:
        df.to_csv(file_name, encoding='utf-8')


#-------------------------------------------------------------------------------
time_marker(text='Complete!')
